from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PyPDF3 import PdfFileReader, PdfFileWriter
from PyPDF3.utils import PdfReadError
import sqlite3
import io
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Database setup
def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "users.db")
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 email TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# init_db()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('login-email')
        password = request.form.get('login-password')
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT id, password FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['email'] = email
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('auth.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('signup-email')
        password = request.form.get('signup-password')
        confirm_password = request.form.get('confirm-password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('auth.html')
        
        if len(password) < 8:
            flash('Password must be at least 8 characters', 'error')
            return render_template('auth.html')
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, hashed_password))
            conn.commit()
            conn.close()
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Email already exists', 'error')
    
    return render_template('auth.html')

@app.route('/auth')
def auth():
    init_db()
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('email', None)
    return redirect(url_for('auth'))

@app.route('/lock', methods=['POST'])
def lock_pdf():
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    
    # --- 1. Enhanced Validation ---
    if 'pdf_file' not in request.files:
        flash('No file uploaded. Please select a PDF file to proceed.', 'error')
        return redirect(url_for('index'))

    file = request.files['pdf_file']
    password = request.form.get('password', '').strip()

    # Validate file
    if not file or file.filename == '':
        flash('No file selected. Please choose a PDF file.', 'error')
        return redirect(url_for('index'))

    if not file.filename.lower().endswith('.pdf'):
        flash('Invalid file type. Only PDF files are accepted.', 'error')
        return redirect(url_for('index'))

    # Validate password
    if not password:
        flash('Password is required to secure your PDF.', 'error')
        return redirect(url_for('index'))
    
    if len(password) < 8:
        flash('Password must be at least 8 characters long for security.', 'error')
        return redirect(url_for('index'))

    # --- 2. Secure PDF Processing ---
    try:
        # Check file size before processing (additional security)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > 16 * 1024 * 1024:  # 16MB limit
            flash('File size exceeds maximum limit of 16MB.', 'error')
            return redirect(url_for('index'))

        # Read PDF with enhanced error handling
        reader = PdfFileReader(file.stream)
        
        # Check if PDF is already encrypted
        if reader.isEncrypted:
            flash('This PDF is already password protected. Please upload an unprotected PDF.', 'error')
            return redirect(url_for('index'))

        # Check for empty PDF
        if reader.getNumPages() == 0:
            flash('The PDF appears to be empty or corrupted.', 'error')
            return redirect(url_for('index'))

        # Create new PDF writer
        writer = PdfFileWriter()

        # Copy all pages with metadata preservation
        for page_num in range(reader.getNumPages()):
            page = reader.getPage(page_num)
            writer.addPage(page)

        # Preserve document info if exists
        if reader.documentInfo:
            writer.addMetadata(reader.documentInfo)

        # Encrypt with stronger algorithm (128-bit AES when available)
        writer.encrypt(
            user_pwd=password,
            owner_pwd=None,  # No separate owner password
            use_128bit=True  # Use stronger encryption when available
        )

        # --- 3. Prepare Secure Download ---
        buffer = io.BytesIO()
        writer.write(buffer)
        buffer.seek(0)

        # Sanitize filename
        original_filename = secure_filename(file.filename)
        locked_filename = f"secured_{original_filename}"

        # Create response with security headers
        response = send_file(
            buffer,
            as_attachment=True,
            download_name=locked_filename,
            mimetype='application/pdf',
            conditional=True
        )

        # Set security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Content-Security-Policy'] = "default-src 'self'"

        # Store success state
        session['last_processed_file'] = locked_filename
        session['processing_success'] = True

        return response

    except PdfReadError:
        flash('The PDF file appears to be corrupted or invalid. Please try with a different PDF file.', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'PDF processing error: {str(e)}', exc_info=True)
        flash('An unexpected error occurred while processing your PDF. Please try again with a different file.', 'error')
        return redirect(url_for('index'))

@app.route('/success')
def success():
    """
    Renders the success page after a successful PDF lock operation.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth'))
    return render_template('success.html')

# if __name__ == '__main__':
#     app.run(debug=True)
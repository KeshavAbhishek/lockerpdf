# 🔐 LockerPDF – Secure PDF Password Protection Web App

LockerPDF is a secure, modern **Flask-based web application** that allows users to **sign up, sign in, and protect PDF files with strong password encryption**.  
The application ensures that files are **never stored on the server**, providing maximum privacy and security.

---

## 🚀 Features

- 🔑 User Authentication (Signup & Login)
- 🔐 Secure PDF Password Protection (AES 128-bit)
- 📄 Supports PDF files up to **16MB**
- 🌙 Dark Mode & ☀️ Light Mode toggle
- 💪 Password strength meter (client-side)
- 🚫 Prevents already encrypted PDFs
- 🧠 Session-based access control
- 🗄️ SQLite database for user management
- 🧼 Clean UI using **Tailwind CSS**
- ⚡ Fast & lightweight (no file storage)

---

## 🧩 Project Structure

- app.py # Main Flask application
- requirements.txt # Python dependencies
- users.db # SQLite database (auto-created)
- static/
  - favicon.ico
- templates/
    - auth.html # Combined Login & Signup UI
    - login.html # Login page
    - signup.html # Signup page
    - index.html # PDF upload & lock page
    - success.html # Success confirmation page
- .gitignore

## 🛠️ Tech Stack

| Layer        | Technology |
|-------------|------------|
| Backend     | Flask (Python) |
| Frontend   | HTML, Tailwind CSS |
| Database   | SQLite |
| PDF Engine | PyPDF3 |
| Security   | Werkzeug Password Hashing |

---

## 📦 Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/lockerpdf.git
cd lockerpdf
```
### 2️⃣ Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Run the Application
```bash
python app.py
```
### 📍 Open your browser at:
```bash
http://127.0.0.1:5000
```

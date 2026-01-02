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
---
# Screenshots
- ## SignUp Screen
  <img width="1919" height="1079" alt="image" src="https://github.com/user-attachments/assets/24305c18-201c-4072-a2d8-c3bc28919f41" />
- ## Login Page
  <img width="1919" height="1079" alt="Screenshot 2026-01-03 033753" src="https://github.com/user-attachments/assets/36d273ba-ef8f-4792-8a0b-7adc7f5c4495" />
- ## Login with Incorrect Details (Error Shown)
  <img width="1919" height="1079" alt="Screenshot 2026-01-03 033811" src="https://github.com/user-attachments/assets/c4d02657-36a3-4cf8-9c4a-a17132e12515" />
- ## After Success Login
  <img width="1919" height="1079" alt="Screenshot 2026-01-03 033826" src="https://github.com/user-attachments/assets/99c80618-8496-4d9c-a0db-d0b81d3d7190" />
- ## File Upload (PDF)
  <img width="1919" height="1031" alt="Screenshot 2026-01-03 033910" src="https://github.com/user-attachments/assets/3d0b3a55-a6cc-4a6c-85af-b008e5b9ac99" />
- ## Entered Password
  <img width="1919" height="1079" alt="Screenshot 2026-01-03 033938" src="https://github.com/user-attachments/assets/0ab5941d-16f3-4b78-86f8-68f30ef67a83" />
- ## Locked PDF Downloaded
  <img width="1919" height="1031" alt="Screenshot 2026-01-03 033958" src="https://github.com/user-attachments/assets/265281ad-fdef-4c77-b919-0acc845474ee" />

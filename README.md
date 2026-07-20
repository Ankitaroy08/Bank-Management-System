# Bank-Management-System
A simple full-stack bank account management app built with Python and Streamlit, refactored from a console script into a clean, validated, web-based UI.  Live demo: add your Streamlit Cloud link here after deploying
Features
Create Account — validates age (18+), email format, and PIN (4 digits), then generates a unique account number
Deposit Money — validates amount, enforces a per-transaction cap
Withdraw Money — prevents overdrafts
Show Details — look up an account by account number + PIN
Update Details — change name, email, or PIN without touching balance/age/account number
Delete Account — permanent deletion with an explicit confirmation step
Tech Stack
Python 3
Streamlit — UI
JSON — lightweight local data storage
hashlib (SHA-256) — PINs are hashed before being stored, never saved in plain text
Project Structure
.
├── app.py      # Streamlit UI — forms, layout, user interaction
├── main.py     # Core logic — validation, hashing, account lookup, JSON persistence
└── data.json   # Auto-created on first run; stores account records

The split between app.py and main.py keeps the UI layer separate from business logic, so the account logic can be tested or reused independently of Streamlit.
Possible Improvements
Swap JSON storage for SQLite or PostgreSQL
Add transaction history per account
Add session-based login instead of re-entering PIN per action
pip install -r requirements.txt

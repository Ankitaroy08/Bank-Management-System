import json
import random
import string
import hashlib
from pathlib import Path

DATABASE = Path(__file__).parent / "data.json"


def load_data() -> list[dict]:
    """Load all accounts from the JSON database. Returns [] if missing/corrupt."""
    if not DATABASE.exists():
        return []
    try:
        with open(DATABASE) as fs:
            return json.loads(fs.read() or "[]")
    except (json.JSONDecodeError, OSError):
        return []


def save_data(data: list[dict]) -> None:
    """Persist all accounts to the JSON database."""
    with open(DATABASE, "w") as fs:
        json.dump(data, fs, indent=2)


def hash_pin(pin: str) -> str:
    """Hash a PIN before it's ever stored on disk."""
    return hashlib.sha256(pin.encode()).hexdigest()


def generate_account_number(existing: list[dict]) -> str:
    """Generate a random account number, retrying on the rare collision."""
    existing_nums = {u["accountNo"] for u in existing}
    while True:
        alpha = random.choices(string.ascii_letters, k=3)
        num = random.choices(string.digits, k=3)
        spchar = random.choices("!@#$%^&*", k=1)
        chars = alpha + num + spchar
        random.shuffle(chars)
        acc_no = "".join(chars)
        if acc_no not in existing_nums:
            return acc_no


def find_user(data: list[dict], acc_no: str, pin: str) -> dict | None:
    """Look up an account by account number + PIN. Returns None if no match."""
    hashed = hash_pin(pin)
    for user in data:
        if user["accountNo"] == acc_no and user["pin"] == hashed:
            return user
    return None


def create_account(data: list[dict], name: str, age: int, email: str, pin: str) -> tuple[bool, str]:
    """
    Validate and create a new account. Mutates `data` and saves on success.
    Returns (success, message_or_account_number).
    """
    if not name.strip():
        return False, "Name cannot be empty."
    if age < 18:
        return False, "You must be 18 or older to open an account."
    if "@" not in email or "." not in email:
        return False, "Please enter a valid email address."
    if not (pin.isdigit() and len(pin) == 4):
        return False, "PIN must be exactly 4 digits."

    account_no = generate_account_number(data)
    info = {
        "name": name.strip(),
        "age": int(age),
        "email": email.strip(),
        "pin": hash_pin(pin),
        "accountNo": account_no,
        "balance": 0,
    }
    data.append(info)
    save_data(data)
    return True, account_no


def deposit(data: list[dict], acc_no: str, pin: str, amount: float) -> tuple[bool, str]:
    user = find_user(data, acc_no, pin)
    if user is None:
        return False, "No account found with that account number and PIN."
    if amount <= 0:
        return False, "Deposit amount must be greater than 0."
    if amount > 10000:
        return False, "You can deposit at most 10,000 in a single transaction."

    user["balance"] += amount
    save_data(data)
    return True, f"Deposited {amount:.2f}. New balance: {user['balance']:.2f}"


def withdraw(data: list[dict], acc_no: str, pin: str, amount: float) -> tuple[bool, str]:
    user = find_user(data, acc_no, pin)
    if user is None:
        return False, "No account found with that account number and PIN."
    if amount <= 0:
        return False, "Withdrawal amount must be greater than 0."
    if amount > user["balance"]:
        return False, "Insufficient balance."

    user["balance"] -= amount
    save_data(data)
    return True, f"Withdrew {amount:.2f}. New balance: {user['balance']:.2f}"


def update_details(
    data: list[dict],
    acc_no: str,
    pin: str,
    new_name: str = "",
    new_email: str = "",
    new_pin: str = "",
) -> tuple[bool, str]:
    user = find_user(data, acc_no, pin)
    if user is None:
        return False, "No account found with that account number and PIN."
    if new_pin and not (new_pin.isdigit() and len(new_pin) == 4):
        return False, "New PIN must be exactly 4 digits."

    warnings = []
    if new_name.strip():
        user["name"] = new_name.strip()
    if new_email.strip():
        if "@" in new_email and "." in new_email:
            user["email"] = new_email.strip()
        else:
            warnings.append("New email looked invalid — email left unchanged.")
    if new_pin:
        user["pin"] = hash_pin(new_pin)

    save_data(data)
    message = "Details updated successfully."
    if warnings:
        message += " (" + " ".join(warnings) + ")"
    return True, message


def delete_account(data: list[dict], acc_no: str, pin: str) -> tuple[bool, str]:
    user = find_user(data, acc_no, pin)
    if user is None:
        return False, "No account found with that account number and PIN."

    data.remove(user)
    save_data(data)
    return True, "Account deleted successfully."

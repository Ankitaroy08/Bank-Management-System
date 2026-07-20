import streamlit as st

import main

st.set_page_config(page_title="Bank Management System", page_icon="🏦", layout="centered")

if "data" not in st.session_state:
    st.session_state.data = main.load_data()

data = st.session_state.data

st.title("🏦 Bank Management System")

menu = st.sidebar.radio(
    "Menu",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Show Details",
        "Update Details",
        "Delete Account",
    ],
)


# ---- Create Account ---------------------------------------------------
if menu == "Create Account":
    st.subheader("Create a New Account")
    with st.form("create_account_form"):
        name = st.text_input("Full name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        email = st.text_input("Email")
        pin = st.text_input("Choose a 4-digit PIN", type="password", max_chars=4)
        confirm_pin = st.text_input("Confirm PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Create Account")

    if submitted:
        if pin != confirm_pin:
            st.error("PIN and confirmation PIN do not match.")
        else:
            success, result = main.create_account(data, name, int(age), email, pin)
            if success:
                st.success("Account created successfully! 🎉")
                st.info(f"**Please save your account number:** `{result}`")
            else:
                st.error(result)


# ---- Deposit ------------------------------------------------------------
elif menu == "Deposit Money":
    st.subheader("Deposit Money")
    with st.form("deposit_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to deposit", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Deposit")

    if submitted:
        success, message = main.deposit(data, acc_no, pin, amount)
        (st.success if success else st.error)(message)


# ---- Withdraw -------------------------------------------------------------
elif menu == "Withdraw Money":
    st.subheader("Withdraw Money")
    with st.form("withdraw_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        amount = st.number_input("Amount to withdraw", min_value=0.0, step=100.0)
        submitted = st.form_submit_button("Withdraw")

    if submitted:
        success, message = main.withdraw(data, acc_no, pin, amount)
        (st.success if success else st.error)(message)


# ---- Show Details ---------------------------------------------------------
elif menu == "Show Details":
    st.subheader("Account Details")
    with st.form("show_details_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Show Details")

    if submitted:
        user = main.find_user(data, acc_no, pin)
        if user is None:
            st.error("No account found with that account number and PIN.")
        else:
            st.success("Account found:")
            st.write(f"**Name:** {user['name']}")
            st.write(f"**Age:** {user['age']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Account Number:** {user['accountNo']}")
            st.write(f"**Balance:** {user['balance']:.2f}")


# ---- Update Details ---------------------------------------------------------
elif menu == "Update Details":
    st.subheader("Update Account Details")
    st.caption("Age, account number, and balance cannot be changed here.")
    with st.form("update_lookup_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("Current PIN", type="password", max_chars=4)
        lookup = st.form_submit_button("Find Account")

    if lookup:
        user = main.find_user(data, acc_no, pin)
        if user is None:
            st.error("No account found with that account number and PIN.")
        else:
            st.session_state["update_target"] = acc_no
            st.session_state["update_pin"] = pin

    target_acc = st.session_state.get("update_target")
    if target_acc:
        with st.form("update_details_form"):
            new_name = st.text_input("New name (leave blank to keep current)")
            new_email = st.text_input("New email (leave blank to keep current)")
            new_pin = st.text_input(
                "New 4-digit PIN (leave blank to keep current)",
                type="password",
                max_chars=4,
            )
            submitted = st.form_submit_button("Save Changes")

        if submitted:
            success, message = main.update_details(
                data,
                target_acc,
                st.session_state["update_pin"],
                new_name,
                new_email,
                new_pin,
            )
            (st.success if success else st.error)(message)
            if success:
                del st.session_state["update_target"]
                del st.session_state["update_pin"]


# ---- Delete Account ---------------------------------------------------------
elif menu == "Delete Account":
    st.subheader("Delete Account")
    st.warning("This action is permanent and cannot be undone.")
    with st.form("delete_form"):
        acc_no = st.text_input("Account number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        confirm = st.checkbox("I understand this will permanently delete my account")
        submitted = st.form_submit_button("Delete Account")

    if submitted:
        if not confirm:
            st.error("Please check the confirmation box to proceed.")
        else:
            success, message = main.delete_account(data, acc_no, pin)
            (st.success if success else st.error)(message)

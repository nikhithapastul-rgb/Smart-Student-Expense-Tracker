
import streamlit as st
import pandas as pd
from datetime import date
from expense_tracker import Expense, Income, ExpenseTracker

# Page configuration
st.set_page_config(
    page_title="Smart Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)

tracker = ExpenseTracker()

st.title("💰 Smart Student Expense Tracker")
st.write("Manage your money smartly and track your daily expenses!")

# Sidebar form
st.sidebar.header("➕ Add Transaction")

with st.sidebar.form("transaction_form"):

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Expense", "Income"]
    )

    amount = st.number_input(
        "Amount (₹)",
        min_value=1.0,
        step=10.0
    )

    if transaction_type == "Expense":
        categories = [
            "Food", "Travel", "Shopping",
            "Education", "Entertainment", "Other"
        ]
    else:
        categories = [
            "Pocket Money", "Scholarship",
            "Part-time Job", "Other"
        ]

    category = st.selectbox("Category", categories)

    transaction_date = st.date_input(
        "Date",
        value=date.today()
    )

    description = st.text_input("Description")

    submit = st.form_submit_button("Save Transaction")

    if submit:
        if not description.strip():
            st.error("Please enter a description.")

        else:
            if transaction_type == "Expense":
                transaction = Expense(
                    amount,
                    category,
                    str(transaction_date),
                    description
                )
            else:
                transaction = Income(
                    amount,
                    category,
                    str(transaction_date),
                    description
                )

            tracker.add_transaction(
                transaction,
                transaction_type
            )

            st.success("Transaction added successfully!")
            st.rerun()


# Read transaction data
records = tracker.get_transactions()
df = pd.DataFrame(records)

# Check CSV columns
if not df.empty:
    required_columns = [
        "Type", "Amount", "Category",
        "Date", "Description"
    ]

    if not all(column in df.columns for column in required_columns):
        st.error("CSV columns are incorrect. Please check expenses.csv.")
        st.stop()

    df["Amount"] = pd.to_numeric(
        df["Amount"], errors="coerce"
    ).fillna(0)

    total_income = df[
        df["Type"] == "Income"
    ]["Amount"].sum()

    total_expenses = df[
        df["Type"] == "Expense"
    ]["Amount"].sum()

else:
    total_income = 0
    total_expenses = 0

balance = total_income - total_expenses


# Financial overview
st.subheader("📊 Financial Overview")

col1, col2, col3 = st.columns(3)

col1.metric(
    "💵 Total Income",
    f"₹{total_income:.2f}"
)

col2.metric(
    "💸 Total Expenses",
    f"₹{total_expenses:.2f}"
)

col3.metric(
    "💰 Balance",
    f"₹{balance:.2f}"
)

st.divider()


# Transaction history
st.subheader("📋 Recent Transactions")

if not df.empty:
    st.dataframe(
        df.sort_values(
            "Date", ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No transactions available yet.")


# Expense analysis
st.subheader("📈 Expense Analysis")

if not df.empty:
    expense_data = df[
        df["Type"] == "Expense"
    ]

    if not expense_data.empty:
        category_data = expense_data.groupby(
            "Category"
        )["Amount"].sum()

        st.bar_chart(category_data)

    else:
        st.info("Add expenses to see your chart.")

else:
    st.info("No expense data available.")


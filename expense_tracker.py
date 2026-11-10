
import csv
import os

# Get the folder where this Python file is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Transaction:
    def __init__(self, amount, category, date, description):
        self.__amount = amount
        self.category = category
        self.date = date
        self.description = description

    def get_amount(self):
        return self.__amount


class Expense(Transaction):
    def show_details(self):
        return {
            "Amount": self.get_amount(),
            "Category": self.category,
            "Date": self.date,
            "Description": self.description
        }


class Income(Transaction):
    def show_details(self):
        return {
            "Amount": self.get_amount(),
            "Category": self.category,
            "Date": self.date,
            "Description": self.description
        }


class ExpenseTracker:
    def __init__(self, filename="data/expenses.csv"):
        self.filename = os.path.join(BASE_DIR, filename)

        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        self.create_file()

    def create_file(self):
        if not os.path.exists(self.filename):
            with open(
                self.filename, "w",
                newline="", encoding="utf-8"
            ) as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Type", "Amount", "Category",
                    "Date", "Description"
                ])

    def add_transaction(self, transaction, transaction_type):
        details = transaction.show_details()

        with open(
            self.filename, "a",
            newline="", encoding="utf-8"
        ) as file:
            writer = csv.writer(file)
            writer.writerow([
                transaction_type,
                details["Amount"],
                details["Category"],
                details["Date"],
                details["Description"]
            ])

    def get_transactions(self):
        records = []

        try:
            with open(
                self.filename, "r",
                newline="", encoding="utf-8-sig"
            ) as file:
                reader = csv.DictReader(file)
                records = list(reader)

        except FileNotFoundError:
            print("File not found!")

        return records

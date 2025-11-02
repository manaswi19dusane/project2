from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import date

app = Flask(__name__)

# ===== Database Connection =====
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",           # your MySQL password (keep empty if none)
    database="bankbuddy.db"   # ✅ correct database name (no .db)
)
cur = conn.cursor(dictionary=True)

# ===== Home Page =====
@app.route('/')
def home():
    return render_template('home.html')

# ===== Add Customer =====
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['mobile']
        address = request.form['city']
        cur.execute(
            "INSERT INTO Customer (Name, Phone, Address) VALUES (%s, %s, %s)",
            (name, phone, address)
        )
        conn.commit()
        return redirect('/view_customers')
    return render_template('add_customer.html')

# ===== View Customers =====
@app.route('/view_customers')
def view_customers():
    cur.execute("SELECT * FROM Customer")
    customers = cur.fetchall()
    return render_template('view_customer.html', customers=customers)

# ===== Deposit =====
@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    # Fetch all accounts for dropdown
    cur.execute("""
        SELECT a.Account_No, c.Name AS customer_name, a.Balance
        FROM Account a
        JOIN Customer c ON a.Customer_ID = c.Customer_ID
    """)
    accounts = cur.fetchall()

    if request.method == 'POST':
        acc_no = request.form['acc_no']
        amount = float(request.form['amount'])

        # Check if account exists
        cur.execute("SELECT Balance FROM Account WHERE Account_No = %s", (acc_no,))
        account = cur.fetchone()
        if account is None:
            return "Error: Account does not exist!"

        # Update balance
        cur.execute("UPDATE Account SET Balance = Balance + %s WHERE Account_No = %s", (amount, acc_no))

        # Record transaction
        cur.execute(
            "INSERT INTO Transaction (Account_No, Type, Amount, Date) VALUES (%s, %s, %s, %s)",
            (acc_no, 'Deposit', amount, date.today())
        )
        conn.commit()
        return "Deposit Successful!"

    return render_template('deposit.html', accounts=accounts)

# ===== Withdraw =====
@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    # Fetch all accounts for dropdown
    cur.execute("""
        SELECT a.Account_No, c.Name AS customer_name, a.Balance
        FROM Account a
        JOIN Customer c ON a.Customer_ID = c.Customer_ID
    """)
    accounts = cur.fetchall()

    if request.method == 'POST':
        acc_no = request.form['acc_no']
        amount = float(request.form['amount'])

        # Check account balance
        cur.execute("SELECT Balance FROM Account WHERE Account_No = %s", (acc_no,))
        account = cur.fetchone()
        if account is None:
            return "Error: Account does not exist!"

        if account['Balance'] >= amount:
            cur.execute("UPDATE Account SET Balance = Balance - %s WHERE Account_No = %s", (amount, acc_no))
            cur.execute(
                "INSERT INTO Transaction (Account_No, Type, Amount, Date) VALUES (%s, %s, %s, %s)",
                (acc_no, 'Withdraw', amount, date.today())
            )
            conn.commit()
            return "Withdrawal Successful!"
        else:
            return "Error: Insufficient Balance!"

    return render_template('withdraw.html', accounts=accounts)

# ===== View Accounts =====
@app.route('/view_accounts')
def view_accounts():
    cur.execute("""
        SELECT a.Account_No, a.Type, a.Balance, c.Name AS customer_name, b.Branch_Name
        FROM Account a
        JOIN Customer c ON a.Customer_ID = c.Customer_ID
        JOIN Branch b ON a.Branch_ID = b.Branch_ID
    """)
    accounts = cur.fetchall()
    return render_template('view_accounts.html', accounts=accounts)

# ===== View Transactions =====
@app.route('/view_transactions')
def view_transactions():
    cur.execute("""
        SELECT t.Transaction_ID, t.Account_No, c.Name AS customer_name, 
               t.Type, t.Amount, t.Date
        FROM Transaction t
        JOIN Account a ON t.Account_No = a.Account_No
        JOIN Customer c ON a.Customer_ID = c.Customer_ID
        ORDER BY t.Transaction_ID DESC
    """)
    transactions = cur.fetchall()
    return render_template('view_transactions.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True)

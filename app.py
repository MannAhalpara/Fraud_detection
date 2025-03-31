from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime
from core import save_transaction

app = Flask(__name__)

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mann@@21122005",  # Change this to your MySQL password
    database="fraud_detection"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_transaction():
    try:
        data = request.json
        print("Received Data:", data)  # Debugging

        cursor = db.cursor()

        # Debug: Check table structure
        cursor.execute("SHOW COLUMNS FROM transaction")
        for column in cursor.fetchall():
            print(column)

        sql = """
        INSERT INTO transaction 
        (transaction_id, sender_account, receiver_account, amount, balance, ip, transaction_type, 
        transaction_success, status, location, trans_time) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data['transactionID'],
            data['senderAccount'],
            data['receiverAccount'],
            data['transactionAmount'],
            data['balance'],
            data['ipAddress'],
            data['transactionType'],  # Must match DB values
            data['transactionSuccess'],
            data['status'],
            data['transactionLocation'],
            datetime.strptime(data['timestamp'], "%Y-%m-%d %H:%M:%S")  # Ensure correct format
        )
        print("Executing SQL:", sql, values)

        save_transaction(data)  # Save to text file
        
        cursor.execute(sql, values)
        db.commit()
        cursor.close()

        return jsonify({"message": "Transaction submitted successfully!"}), 200

    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

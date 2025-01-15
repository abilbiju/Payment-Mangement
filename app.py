from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from collections import Counter

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("sturdy-magnet-438213-h5-d2694925817e.json", scopes=scope)
client = gspread.authorize(creds)
items_sheet = client.open_by_key("1vEmJoc-fhjGIK0L5vMsBs5xmm88NXzVRpHFUboqRuPA").sheet1
payments_sheet = client.open_by_key("1s68NAJ-L1hj9vf6JzNRwK9QYS3Jseu9VprCM1c7UeTg").sheet1

@app.route('/')
def index():
    items = items_sheet.get_all_records()
    return render_template('index.html', items=items)

@app.route('/admin')
def admin():
    items = items_sheet.get_all_records()
    return render_template('admin.html', items=items)

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    items_sheet.append_row([name, price])
    return redirect(url_for('admin'))

@app.route('/edit_item/<int:row>', methods=['POST'])
def edit_item(row):
    name = request.form['name']
    price = request.form['price']
    items_sheet.update_cell(row + 1, 1, name)
    items_sheet.update_cell(row + 1, 2, price)
    return redirect(url_for('admin'))

@app.route('/delete_item/<int:row>')
def delete_item(row):
    items_sheet.delete_rows(row + 1)
    return redirect(url_for('admin'))

@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    items = request.form.get('items').split(',')
    quantities = request.form.get('quantities').split(',')
    amounts = request.form.get('amounts').split(',')
    timestamp = str(datetime.utcnow())
    for item, quantity, amount in zip(items, quantities, amounts):
        if item:  # Ensure item is not empty
            payments_sheet.append_row([item, float(amount), timestamp, int(quantity)])
    return redirect(url_for('index'))

@app.route('/get_statistics')
def get_statistics():
    payments = payments_sheet.get_all_records()
    item_counts = Counter()
    total_revenue = 0.0
    for payment in payments:
        item_counts[payment['item_name']] += int(payment['quantity'])  # Ensure 'quantity' is referenced correctly
        total_revenue += float(payment['amount'])
    labels = list(item_counts.keys())
    values = list(item_counts.values())
    return jsonify(labels=labels, values=values, total_revenue=total_revenue)

if __name__ == '__main__':
    app.run(debug=True)
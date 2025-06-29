from flask import Flask, render_template, request, redirect, url_for, session
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong key

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ADMIN_USERNAME = 'surendra'
ADMIN_PASSWORD = '797685'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        age = request.form.get('age')
        mobile = request.form.get('mobile')
        whatsapp = request.form.get('whatsapp')
        gmail = request.form.get('gmail')
        education = request.form.get('education')
        bank_name = request.form.get('bank_name')
        account = request.form.get('account')
        ifsc = request.form.get('ifsc')
        phonepay = request.form.get('phonepay')
        parcel_address = request.form.get('address')
        id_type = "Aadhar"

        rusem_pdf = request.files.get('rusemPdf')
        filename = ''
        if rusem_pdf and rusem_pdf.filename != '':
            safe_filename = secure_filename(rusem_pdf.filename)
            filename = f"{fullname.replace(' ', '_')}_{safe_filename}"
            rusem_pdf.save(os.path.join(UPLOAD_FOLDER, filename))

        file_exists = os.path.isfile('submissions.csv')
        with open('submissions.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow([
                    'Full Name', 'Age', 'Mobile', 'WhatsApp', 'Gmail', 'Education',
                    'Bank Name', 'Account', 'IFSC', 'PhonePay', 'ID Type',
                    'PDF Filename', 'Parcel Address'
                ])
            writer.writerow([
                fullname, age, mobile, whatsapp, gmail, education,
                bank_name, account, ifsc, phonepay, id_type,
                filename, parcel_address
            ])

        return render_template('index.html', thank_you=True)

    return render_template('index.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            error = "Invalid credentials. Please try again."
    return render_template('admin_login.html', error=error)

@app.route('/admin')
def admin_panel():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
    data = []
    if os.path.exists('submissions.csv'):
        with open('submissions.csv', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
    return render_template('admin_panel.html', data=data)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run()

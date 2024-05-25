# app.py
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import NumberRange
import os
from generate_invoice import create_invoice

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'invoices'

chocolates = {
    'huzzelnut': {'name': 'Huzzelnut Chocolate', 'price': 100},
    'milk': {'name': 'Milk Chocolate', 'price': 150},
    'dark': {'name': 'Dark Chocolate', 'price': 200},
    'frey': {'name': 'Frey Chocolate', 'price': 99},
    'lindt': {'name': 'Lindt Chocolate', 'price': 169},
    'cailler': {'name': 'Cailler Chocolate', 'price': 299}
}

class OrderForm(FlaskForm):
    huzzelnut_qty = IntegerField('Huzzelnut Quantity', validators=[NumberRange(min=0)])
    milk_qty = IntegerField('Milk Quantity', validators=[NumberRange(min=0)])
    dark_qty = IntegerField('Dark Quantity', validators=[NumberRange(min=0)])
    frey_qty = IntegerField('Frey Quantity', validators=[NumberRange(min=0)])
    lindt_qty = IntegerField('Lindt Quantity', validators=[NumberRange(min=0)])
    cailler_qty = IntegerField('Cailler Quantity', validators=[NumberRange(min=0)])
    submit = SubmitField('Buy Now')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    if form.validate_on_submit():
        quantities = {
            'huzzelnut': form.huzzelnut_qty.data,
            'milk': form.milk_qty.data,
            'dark': form.dark_qty.data,
            'frey': form.frey_qty.data,
            'lindt': form.lindt_qty.data,
            'cailler': form.cailler_qty.data
        }
        total_price = sum(quantities[choco] * chocolates[choco]['price'] for choco in chocolates)
        return redirect(url_for('payment', quantities=quantities, total_price=total_price))
    return render_template('index.html', form=form, chocolates=chocolates)

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        quantities = {choco: int(qty) for choco, qty in request.form.items() if choco in chocolates}
        total_price = int(request.form['total_price'])
        invoice_id = create_invoice(quantities, total_price, chocolates)
        return redirect(url_for('download_invoice', invoice_id=invoice_id))
    
    quantities = request.args.get('quantities')
    total_price = request.args.get('total_price')
    if quantities:
        quantities = eval(quantities)
    else:
        quantities = {}
    
    chosen_chocolates = {choco: {'name': chocolates[choco]['name'], 'quantity': quantities.get(choco, 0)} for choco in chocolates}
    return render_template('payment.html', quantities=quantities, total_price=total_price, chosen_chocolates=chosen_chocolates)

@app.route('/invoice/<invoice_id>')
def download_invoice(invoice_id):
    return send_from_directory(app.config['UPLOAD_FOLDER'], invoice_id)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)

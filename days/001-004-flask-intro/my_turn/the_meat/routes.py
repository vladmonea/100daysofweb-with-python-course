from flask import render_template

from the_meat import app


@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html', name='Vlad')


@app.route('/add')
@app.route('/add/<num1>/<num2>')
def add(num1=None, num2=None):
    if not num1 or not num2:
        return "Please enter the number in the URL in the form /num1/num2"
    res = int(num1) + int(num2)
    return render_template('add.html', title='Add!', num1=num1, num2=num2, res=res)


@app.route('/subtract')
@app.route('/subtract/<num1>/<num2>')
def subtract(num1=None, num2=None):
    if not num1 or not num2:
        return "Please enter the number in the URL in the form /num1/num2"
    res = int(num1) - int(num2)
    return render_template('subtract.html', title='Subtract!', num1=num1, num2=num2, res=res)


@app.route('/multiply')
@app.route('/multiply/<num1>/<num2>')
def multiply(num1=None, num2=None):
    if not num1 or not num2:
        return "Please enter the number in the URL in the form /num1/num2"
    res = int(num1) * int(num2)
    return render_template('multiply.html', title='Multiply!', num1=num1, num2=num2, res=res)


@app.route('/divide')
@app.route('/divide/<num1>/<num2>')
def divide(num1=None, num2=None):
    if not num1 or not num2:
        return "Please enter the number in the URL in the form /num1/num2"
    res = int(num1) / int(num2) if int(num2) != 0 else 'Nah-ah-ah! we do not divide by zero in this house!'
    return render_template('divide.html', title='Divide!', num1=num1, num2=num2, res=res)

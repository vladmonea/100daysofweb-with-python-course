"""Utility functions"""
from flask import render_template
from functools import wraps

def check_inputs(name):
    def decorator(func):
        @wraps(func)
        def check_valid(num1=None, num2=None):
            if not num1 or not num2:
                msg = "Please enter the number in the URL in the form /num1/num2"
                return render_template('error_page.html', msg=msg)
            return func(num1, num2)
        return check_valid
    return decorator

import os
from flask import Flask
import random
from flask import render_template
app = Flask(__name__)
@app.route('/')
def hello():
    return 'Hello World'

@app.route('/auth')
def auth(name=None):
    return render_template('quickstart.html', name=name)

@app.route('/score/<int:email_order>')
def email(email_order):
    return str(random.randint(1,10))

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
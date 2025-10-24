from flask import Flask, render_template, request
import requests  # NOT the same as requests 
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template('index.html')

@app.route('/get_recipes')
def get_recipes():



    
if __name__ == '__main__':
    app.run()
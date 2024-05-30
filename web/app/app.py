import os
from flask import Flask, render_template

template_dir = os.path.abspath("templates")
static_dir   = os.path.abspath("static")
app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

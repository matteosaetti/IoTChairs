import os
from flask import Flask, render_template

template_dir = os.path.abspath("web/templates")
static_dir   = os.path.abspath("web/static")
app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)

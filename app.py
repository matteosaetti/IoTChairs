import os
from flask import Flask, render_template

# Crea un'applicazione Flask
template_dir = os.path.abspath("web/templates")
static_dir   = os.path.abspath("web/static")
app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)

# Definisci una rotta per la homepage
@app.route('/')
def home():
    return render_template("index.html")

# Avvia il server Flask
if __name__ == '__main__':
    app.run(debug=True)

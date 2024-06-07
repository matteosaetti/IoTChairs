import os
from flask import Flask, render_template
# docker network create --driver=bridge --subnet=172.42.0.0/24 --gateway=172.42.0.1 docker_net
template_dir = os.path.abspath("app/templates")
static_dir   = os.path.abspath("app/static")
app = Flask(__name__, template_folder=template_dir,static_url_path='', static_folder=static_dir)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

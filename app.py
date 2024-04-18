from flask import Flask

# Crea un'applicazione Flask
app = Flask(__name__)

# Definisci una rotta per la homepage
@app.route('/')
def home():
    return "Benvenuto alla nostra pagina web!"

# Avvia il server Flask
if __name__ == '__main__':
    app.run(debug=True)

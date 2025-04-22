from flask import Flask, render_template, g
import sqlite3

app = Flask(__name__)
DATABASE = 'collections.db'

# Conexão com o banco
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Lista de coleções
@app.route('/collections')
def db_list():
    db = get_db()
    cur = db.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = [row['name'] for row in cur.fetchall()]
    return render_template('db_list.html', tables=tables)

# Detalhes de itens
@app.route('/collection/<name>')
def item_detail(name):
    db = get_db()
    try:
        cur = db.execute(f'SELECT * FROM {name}')
        items = cur.fetchall()
        return render_template('item_detail.html', name=name, items=items)
    except Exception as e:
        return f"Erro ao acessar a coleção {name}: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

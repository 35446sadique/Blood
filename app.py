from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('blood.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS donors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        blood_group TEXT,
        city TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS blood_banks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        city TEXT,
        phone TEXT
    )
''')


cursor.execute("INSERT OR IGNORE INTO donors VALUES (1, 'Tom', '555-1111', 'A+', 'Kerala')")
cursor.execute("INSERT OR IGNORE INTO donors VALUES (2, 'Riya', '555-2222', 'O-', 'Karnataka')")
cursor.execute("INSERT OR IGNORE INTO blood_banks VALUES (1, 'City Blood Bank', '123 Main St', 'Kerala', '555-0001')")
cursor.execute("INSERT OR IGNORE INTO blood_banks VALUES (2, 'Central Blood Center', '456 Oak Ave', 'Karnataka', '555-0002')")
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        blood_group = request.form['blood_group']
        city = request.form['city']
        
        conn = sqlite3.connect('blood.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO donors (name, phone, blood_group, city) VALUES (?, ?, ?, ?)',
                     (name, phone, blood_group, city))
        conn.commit()
        conn.close()
        
        return redirect('/donors')
    
    return render_template('register.html')

@app.route('/donors')
def donors():
    blood_group = request.args.get('blood_group', '')
    city = request.args.get('city', '')
    
    conn = sqlite3.connect('blood.db')
    cursor = conn.cursor()
    
    if blood_group and city:
        donors = cursor.execute('SELECT * FROM donors WHERE blood_group=? AND city LIKE ?', 
                              (blood_group, f'%{city}%')).fetchall()
    elif blood_group:
        donors = cursor.execute('SELECT * FROM donors WHERE blood_group=?', (blood_group,)).fetchall()
    elif city:
        donors = cursor.execute('SELECT * FROM donors WHERE city LIKE ?', (f'%{city}%',)).fetchall()
    else:
        donors = cursor.execute('SELECT * FROM donors').fetchall()
    
    conn.close()
    return render_template('donors.html', donors=donors, blood_group=blood_group, city=city)

@app.route('/bloodbanks')
def bloodbanks():
    city = request.args.get('city', '')
    
    conn = sqlite3.connect('blood.db')
    cursor = conn.cursor()
    
    if city:
        banks = cursor.execute('SELECT * FROM blood_banks WHERE city LIKE ?', (f'%{city}%',)).fetchall()
    else:
        banks = cursor.execute('SELECT * FROM blood_banks').fetchall()
    
    conn.close()
    return render_template('bloodbanks.html', banks=banks, city=city)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
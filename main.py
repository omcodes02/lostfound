from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret123"

# DATABASE
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="lost_found",
    auth_plugin='mysql_native_password',
    charset='utf8',
    use_unicode=True
)

cursor = db.cursor()

# ================= SIGNUP =================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    if request.method == 'POST':
        try:
            cursor.execute("""
            INSERT INTO users (username,password,stream,class,roll_no,email)
            VALUES (%s,%s,%s,%s,%s,%s)
            """, (
                request.form['username'],
                request.form['password'],
                request.form['stream'],
                request.form['class'],
                request.form['roll_no'],
                request.form['email']
            ))
            db.commit()
            return redirect('/login')
        except:
            msg = " Username already exists"

    return render_template("signup.html", message=msg)

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == 'POST':
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s",
                       (request.form['username'], request.form['password']))
        user = cursor.fetchone()

        if user:
            session['user'] = user[1]
            session['email'] = user[6]
            return redirect('/')
        else:
            msg = "Invalid Username or Password"

    return render_template("login.html", message=msg)

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

# ================= HOME =================
@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM lost_items")
    items = cursor.fetchall()

    return render_template("index.html", items=items)

# ================= ADD =================
@app.route('/add')
def add():
    if 'user' not in session:
        return redirect('/login')
    return render_template("add.html")

@app.route('/add_item', methods=['POST'])
def add_item():
    cursor.execute("""
    INSERT INTO lost_items (item_name,description,location,date_lost,contact_email)
    VALUES (%s,%s,%s,%s,%s)
    """, (
        request.form['item_name'],
        request.form['description'],
        request.form['location'],
        request.form['date_lost'],
        session['email']
    ))
    db.commit()
    return redirect('/')

# ================= DELETE =================
@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM lost_items WHERE id=%s", (id,))
    db.commit()
    return redirect('/')

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
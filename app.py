from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)

#Mysql Conection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'YOUR_PASSWORD'
app.config['MYSQL_DB'] = 'flasklogin'
mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'


#My routes
@app.route('/')
def home():
    return render_template("home.html")



@app.route('/register', methods=["GET", "POST"])
def register():
    
    if request.method == 'GET':
        return render_template("register.html")
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password,))
        mysql.connection.commit()
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        return redirect(url_for('contactss'))


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if len(user) > 0:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['name'] = user['name']
                session['email'] = user['email']
                return render_template("contacts.html")
            else:
                flash("Error password and email not match")
                return redirect(url_for('login'))
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

###CONTACTS

@app.route('/contacts')
def contactss():
    #cursor me permite ejecutar las conusltas de mysql
    cur = mysql.connection.cursor()
    #Trae los datos 
    cur.execute('SELECT * FROM contacts')
    #ejecutar la consulta y obtener todos los datos
    data = cur.fetchall()
    return render_template("contacts.html", contacts = data)


@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        #cursor me permite ejecutar las conusltas de mysql
        cur = mysql.connection.cursor()
        #consulta para insertar un nuevo dato
        cur.execute('INSERT INTO contacts (fullname,phone,email) VALUES (%s, %s, %s)',(fullname,phone,email))
        #funcion para ejecutar la consulta
        mysql.connection.commit()
        #envia un mensaje flash
        flash('Contact added successfully')
        return redirect(url_for('contactss'))

#EDIT
@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

#UPDATE OF EDIT
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        #funcion para ejecutar la consulta
        mysql.connection.commit()
        flash('Contact Update Successfully')
        return redirect(url_for('contactss'))

#DELETE
@app.route('/delete/<string:id>') #recibe una ruta con un id
def delete_contact(id): #recibe ese id
    #conexion
    cur = mysql.connection.cursor()
    #borra el id que se le esta pasando
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    #funcion para ejecutar la consulta
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('contactss'))


@app.route('/logout')
def logout():
    session.clear()
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)

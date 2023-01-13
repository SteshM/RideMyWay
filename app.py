from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'RideMyWay'

mysql =MySQL(app)

@app.route("/register/user", methods=["POST"])
def register():
    try:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        email = request.json['email']
        password = request.json['password']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users(first_name, last_name,email,password) VALUES(%s,%s,%s,%s)",(first_name,last_name,email,password))

        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "User successfully registered"})
    except :
        return jsonify({"message":"This Email already exists!"})
    





@app.route("/") 
def home():
    return "Hello world yeeey !"

if __name__ == "__main__":
    app.run(debug=True)

    
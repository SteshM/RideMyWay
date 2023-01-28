from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
app = Flask(__name__)



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'RideMyWay'

mysql =MySQL(app)

   #REGISTER
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


  #LOGIN

@app.route("/login", methods=["POST"])
def login():
    email = request.json['email']
    app.logger.info("email %s",email)
    password = request.json['password']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM users where email = %s',[email])
    record = cursor.fetchone()
    app.logger.info("record %s" , record)
    app.logger.info("password %s" , record[4])
    app.logger.info("first_name %s" , record[1])
    

    if record == None:
        return jsonify ({'message': "Email doesn't exist"})

    elif password == record[4]:
            return jsonify({'message': 'Login successful'})
    
    else:
         return jsonify({'message': 'Incorrect password'})


@app.route('/rides', methods=['GET'])
def getRide():

 # Create a list to store the results
    ride_list = []

    # Iterate through the data and append each item to the list
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM rides")
    record = cursor.fetchall() 
    counter = 1
    app.logger.info("-------------------------------------------------------------------------------------------------------")
    for ride in record:
        for column in ride:
            app.logger.info(" row:%s  | column:%s" ,counter, column)
        
        for column in ride:
            app.logger.info("------------------")

        



        ride_list.append({
            'id': ride[0],
            'origin':ride[3],
            'destination':ride[4],
            'departure_time':str(ride[6]),
        })
        counter+=1


    # Return the list of rides
    return jsonify(ride_list)


@app.route("/") 
def home():
    return "Hello world yeeey !"

if __name__ == "__main__":
    app.run(debug=True)

    
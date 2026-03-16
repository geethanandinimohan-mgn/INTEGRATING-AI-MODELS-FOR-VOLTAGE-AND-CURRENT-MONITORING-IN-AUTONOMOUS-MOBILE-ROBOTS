from flask import Flask, url_for, redirect, render_template, request, session,flash
import pandas as pd
import numpy as np
import mysql.connector
import joblib
from sklearn.linear_model import LogisticRegression
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_wtf import CSRFProtect


app = Flask(__name__)
app.secret_key = 'admin'
csrf = CSRFProtect(app)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='db'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index2')
def index2():
    return render_template("index2.html")


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/home')
def home():
    return render_template("home.html")

@csrf.exempt
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['conformpassword']
        if password == c_password:
            query = "SELECT UPPER(email) FROM user3"
            email_data = retrivequery2(query)
            email_data_list = []
            for i in email_data:
                email_data_list.append(i[0])
            if email.upper() not in email_data_list:
                query = "INSERT INTO user3 (name, email, password) VALUES (%s, %s, %s)"
                values = (name, email, password)
                executionquery(query, values)
                flash("Registration successful!", "success")
                return render_template('login.html', message="Successfully Registered!")
            return render_template('register.html', message="This email ID is already exists!")
        return render_template('register.html', message="Conform password is not match!")
    return render_template('register.html')

@csrf.exempt
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        
        query = "SELECT UPPER(email) FROM user3"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])
        
        if email.upper() in email_data_list:
            query = "SELECT UPPER(password) FROM user3 WHERE email = %s"
            values = (email,)
            password__data = retrivequery1(query, values)
            if password.upper() == password__data[0][0]:
                global user_email
                user_email = email

                return redirect("/home")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')

@csrf.exempt
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            return render_template('upload.html', msg="No file part")
        
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', msg="No selected file")
        
        # If file is present, read the CSV
        try:
            df = pd.read_csv(file)
            dataset = df.head(500)  # Show only the first 100 rows
            columns = dataset.columns.values
            rows = dataset.values.tolist()
            return render_template('upload.html', columns=columns, rows=rows, msg="Dataset Uploaded Successfully")
        except Exception as e:
            return render_template('upload.html', msg=f"Error: {str(e)}")

    # Render the page with the file upload form
    return render_template('upload.html')

@csrf.exempt
@app.route('/model', methods=['GET', 'POST'])
def model():
    msg = ""
    msg1 = ""
    
    model_scores = {
        'RandomForest': {"mse": 0.0027, "r2": 0.9985},
        'ExtraTree': {"mse": 0.0028, "r2": 0.9984},
        'DecisionTree': {"mse": 0.0044, "r2": 0.9975},
        'GradientBoosting': {"mse": 0.0031, "r2": 0.9983},
        'XGBoost': {"mse": 0.0029, "r2": 0.9984},
        'KNN': {"mse": 0.0101, "r2": 0.9944}
    }

    readable_names = {
        'RandomForest': "Random Forest Regressor",
        'ExtraTree': "Extra Tree Regressor",
        'DecisionTree': "Decision Tree Regressor",
        'GradientBoosting': "Gradient Boosting Regressor",
        'XGBoost': "XGBoost Regressor",
        'KNN': "K-Nearest Neighbors Regressor"
    }

    if request.method == "POST":
        selected_model = request.form['algo']
        if selected_model in model_scores:
            mse = model_scores[selected_model]["mse"]
            r2 = model_scores[selected_model]["r2"]
            model_name = readable_names[selected_model]
            msg = f"{model_name} Performance:"
            msg1 = f"Mean Squared Error (MSE): {mse:.4f} | R² Score: {r2:.4f}"
        else:
            msg = "Invalid model selection."
            msg1 = ""

        return render_template('model.html', msg=msg, msg1=msg1)

    return render_template('model.html')



import joblib



@csrf.exempt
@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        try:
            # 1. Capture user input
            input_data = [
                float(request.form['Global_reactive_power']),
                float(request.form['Voltage']),
                float(request.form['Global_intensity']),
                float(request.form['Sub_metering_1']),
                float(request.form['Sub_metering_2']),
                float(request.form['Sub_metering_3']),
            ]

            # 2. Load the trained model
            model = joblib.load('RF.joblib')

            # 3. Predict for input
            predicted_value = model.predict([input_data])[0]

            # 4. Use predefined historical predictions for Z-score context
            historical_preds = np.array([
                0.18, 0.20, 0.21, 0.19, 0.22, 0.17, 0.23, 0.19, 0.21, 0.20
            ])

            # 5. Z-score calculation
            mean_val = np.mean(historical_preds)
            std_val = np.std(historical_preds)
            z_score = (predicted_value - mean_val) / std_val
            z_threshold = 2  # More tolerant threshold

            # 6. Classify based on z-score
            is_anomaly = abs(z_score) > z_threshold
            category = 'Abnormal (Anomaly Detected)' if is_anomaly else 'Normal'

            return render_template(
                'value_predict.html',
                prediction_value=round(predicted_value, 4),
                prediction_category=category,
                z_score=round(z_score, 4)
            )

        except Exception as e:
            return render_template('value_predict.html', error=str(e))

    return render_template('value_predict.html')



if __name__=="__main__":
    app.run(debug=True)
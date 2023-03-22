#importing Flask library
from flask import Flask, request, jsonify, render_template

#Initializing Flask 
app = Flask(__name__)

#Route --> By default it takes GET request
@app.route("/") #homepage
#function to define
def home_page():
    return render_template("index.html") #will extract html file from templates

#Route-2
@app.route("/aboutus")
def aboutus():
    return "Welcome to Ayush"

#Routing with POST request
@app.route("/demo", methods = ["POST"])
def math_operator():
    if (request.method == "POST"): #request will store in form of POST
        operation = request.json["operation"] #initializing operation in form of "jsonify"
        num1 = int(request.json["num1"]) #extracting num1
        num2 = int(request.json["num2"]) #extracting num2
        result = 0
        
        if operation == "add": #for addition operation
            result = num1 + num2
        elif operation == "sub": #for subtraction operation
            result = num1 - num2
        elif operation == "mul": #for multiplication operation
            result = num1 * num2
        elif operation == "div": #for division operation
            result = num1 / num2
        else:
            result = "Not an mathematical operation"
        
        return jsonify(f"The operation is {operation} & result is {result}")

@app.route("/operation", methods = ["POST"])
def final_operator():
    if (request.method == "POST"): #request will store in form of POST
        operation = request.form["operation"] #initializing operation in form of "html"
        num1 = int(request.form["num1"]) #extracting num1
        num2 = int(request.form["num2"]) #extracting num2
        result = 0
        
        if operation == "add": #for addition operation
            result = num1 + num2
        elif operation == "sub": #for subtraction operation
            result = num1 - num2
        elif operation == "mul": #for multiplication operation
            result = num1 * num2
        elif operation == "div": #for division operation
            result = num1 / num2
        else:
            result = "Not an mathematical operation"
        
        return render_template("result.html", result = result)

#entry point for flask
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000) #host -> Local address, Port -> to acess the application 
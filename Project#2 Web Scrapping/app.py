#importing libraries
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request  import urlopen as UReq
import logging 

#initializing the logging level 
logging.basicConfig(filename = "log_file.log", level = logging.INFO) 

#initializing Flask
app = Flask(__name__)

#initializing home page with app route
@app.route('/',methods=['GET'])  
def homePage():
    return render_template("index.html")

#routing the app
@app.route('/review',methods=['POST','GET']) # route to show the review comments in a web UI
def index():
    if request.method == 'POST':
        try:
            search_string = request.form["content"].replace(" ", "") #accepting the request
            flipkart_url = "https://www.flipkart.com/search?q=" + search_string #concatnatig with search with flipkart
            uclient = UReq(flipkart_url) #Requestin URL lib
            page = uclient.read() #to read the request
            uclient.close() #closing the request 
            flipkart_html = bs(page, "html.parser") #reading the request in beautiful format with the better format
            bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"}) #reading the first request
            del bigboxes[0:3] #deleting 1st informations as it doesn't contains useful info
            box = bigboxes[0] #reading the first product of the site
            product_link = "https://www.flipkart.com" + box.div.div.div.a['href'] #to reach out the 1st product
            product_req = requests.get(product_link) #requesting link in the form of request
            product_html = bs(product_req.text, "html.parser") #reading the code in define manner
            logging.info("product_html") #logging the product html file
            
            #to add all information in csv file to make
            file = search_string + ".csv"
            fw = open(file, "w")
            headers = "Product, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)            
            
            #moving through the review section
            comment_boxes = product_html.find_all('div', {'class': "_16PBlm"})
            #moving through all section 
            reviews = []
            for i in comment_boxes:
                
                #name section
                try:
                    name = i.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = "no name"
                    
                #rating
                try:
                    rating = i.div.div.div.div.text
                except:
                    rating = "no rating"

                #review header
                try:
                    header = i.div.div.div.p.text
                except:
                    header = "no header"
                
                #customer comment    
                try:
                    comtag = i.div.div.find_all('div', {'class': ''})
                    
                    cust_comment = comtag[0].div.text
                except Exception as e:
                    logging.info(e)

                #creating dictonary
                mydict = {"Product": search_string, "Name": name, "Rating": rating, "CommentHead": header, "Comment": cust_comment}            
                reviews.append(mydict)
                
            return render_template('result.html', reviews=reviews[0:(len(reviews)-1)])
        
        except Exception as e: #excepting if something failed in the log
            logging.info(e)

    else:
        return render_template('index.html') #returning to our original template
   

#running the flask 
if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
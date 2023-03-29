from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import pymongo
import os

#logging the file
import logging
logging.basicConfig(filename="scrapper.log" , level=logging.INFO)

#initializing the Flask
app = Flask(__name__)

#home page
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

#defining review page
@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
                try:#for searching the images
                    query = request.form['content'].replace(" ","")

                    #to save images
                    save_directory = "images/"

                    #create directory if doesn't exist
                    if not os.path.exists(save_directory):
                        os.makedirs(save_directory)

                    #to get avoid by Google 
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
                    #fetch the search page
                    response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M")
                    #parsing the html using bs
                    soup = BeautifulSoup(response.content, "html.parser")
                    #find all img tags
                    image_tags = soup.find_all("img")
                    #saving the image
                    del image_tags[0]
                    img_data=[]
                    for index,image_tag in enumerate(image_tags):
                                #getting url source
                                image_url = image_tag['src']
                                # sending url request to save
                                image_data = requests.get(image_url).content
                                mydict={"Index":index,"Image":image_data}
                                img_data.append(mydict)
                                
                                #opening the path
                                with open(os.path.join(save_directory, f"{query}_{image_tags.index(image_tag)}.jpg"), "wb") as f:
                                    f.write(image_data)
                    
                    #for saving the mongodb client                
                    client = pymongo.MongoClient("mongodb+srv://ayushgandhi904:<password>@cluster0.9znn17h.mongodb.net/?retryWrites=true&w=majority")
                    db = client['image_scrap']
                    review_col = db['image_scrap_data']
                    review_col.insert_many(img_data)          

                    return "image laoded in pc"
                
                #if an exception
                except Exception as e:
                    logging.info(e)
                    return 'something is wrong'


    else:
        return render_template('index.html')

#running flask
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
from flask import Flask, render_template,request
import requests
from bs4 import BeautifulSoup as bs
import os
app = Flask(__name__)

@app.route('/', methods=["GET"])
def home():
    return render_template("index.html")

@app.route('/about', methods = ['POST','GET'])
def about():
    if(request.method == "POST"):
        try:
            query = request.form['content'].replace(" ","")
            save_dir = "images/"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir) 

            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
            response = requests.get(f"https://www.google.com/search?q={query}&sxsrf=AJOqlzUuff1RXi2mm8I_OqOwT9VjfIDL7w:1676996143273&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiq-qK7gaf9AhXUgVYBHYReAfYQ_AUoA3oECAEQBQ&biw=1920&bih=937&dpr=1#imgrc=1th7VhSesfMJ4M",headers=headers)
            soup = bs(response.content,'html.parser')
            image_tag = soup.find_all("img")
            del image_tag[0]
            img_data_mongo = []
            
            for i in image_tag:
                img_url = i.get('data-src')or i.get("src") 
                img_data = requests.get(img_url).content
                mydict={"Index":i,"Image":img_data}
                img_data_mongo.append(mydict)
                with open(os.path.join(save_dir, f"{query}_{image_tag.index(i)}.jpg"), "wb") as f:
                    f.write(img_data)
                
            return "Image Downloaded Complete"
                                               
        except Exception as e:
            return e
    else:
        return "Something Wrong"

if __name__ == '__main__':
    app.run(debug=True)



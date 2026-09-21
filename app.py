from flask import Flask, request,render_template,redirect,url_for,jsonify
import requests
from bs4 import BeautifulSoup
import json
from flask import abort
import os
app = Flask(__name__)

if(os.path.exists("words.json")==False):
    with open("words.json","w",encoding="utf-8") as file:
        json.dump({},file,ensure_ascii=False)

@app.route("/words")
def words():
    with open("words.json","r",encoding="utf-8") as file:
        data = json.load(file)
        
        newC= data.keys()
        

    return render_template("word.html",content=newC)

@app.route("/",methods=["GET"])
def eng():
    with open("words.json","r",encoding="utf-8") as file:
        data = json.load(file)
        number=len(data.keys())
    
    return render_template("index.html",num=number)
    
    
   

@app.route("/control",methods=["POST"])
def control():
    data = request.get_json()
    word = data["word"]
    status = bool
    alert =""
    number=0
    
    if word =="" or word ==None:
        status =False
        alert=  "not"
    else: 

        status=True
        if(os.path.exists("words.json")):  #re-checking
            with open("words.json","r",encoding="utf-8") as file:  
                data = json.load(file)

            if word in data:
                status=False
                alert=  "al-exist"

        else:
            data={}
        
        
    
       
        if status:

        

        
            url = f"https://freedictionaryapi.com/api/v1/entries/en/{word}"
            
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers)
            jsonv=response.json()

            if jsonv["entries"] != []:
                
                
                if(status):

                    data[word] =jsonv["entries"][0]["senses"][0]["definition"]

                    status=True
                    alert=  "exist"

                    with open("words.json","w",encoding="utf-8") as file :
                        json.dump(data,file, indent=4, ensure_ascii=False)
                    

                
            else:
                status =False
                alert=  "not"

            with open("words.json","r",encoding="utf-8") as file:
                   data = json.load(file)
                   number = len(data.keys())

    return jsonify({
            "status":status,"num" :number,"alert":alert
        })

@app.route("/words/<string:name>",methods=["GET"])
def detail(name):
    
    with open("words.json","r",encoding="utf-8") as file:
        data=json.load(file)
        if name in data:
            description=data[name]
        else:
            abort(404)
            return 

    return render_template("detail.html",description=description,name=name)

if __name__ == "__main__":
    app.run(debug=True)
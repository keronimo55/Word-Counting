from flask import Flask, request,render_template,redirect,url_for
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
@app.route("/")
def home():
    return "Hello World!"


@app.route("/eng",methods=["GET","POST"])
def eng():
    word= ""
    if request.method=="GET":
        status=request.args.get("status")
        
        if status is None:
            status=""
        
        return render_template("index.html",status=status)
    
    else:
        word=request.form.get("word") 
        if word =="":
            status =False
        else: 
            url = f"https://freedictionaryapi.com/api/v1/entries/en/{word}"
            
            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers)
            json=response.json()

            if json["entries"] != []:
                status=True
            else:
                status =False
        
       

        return redirect(url_for("eng",status=status))
    

if __name__ == "__main__":
    app.run(debug=True)
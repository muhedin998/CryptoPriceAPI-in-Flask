from flask import Flask, render_template
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json, requests

app  = Flask(__name__)

@app.route('/')
def index():
    req = requests.get("http://data.fixer.io/api/latest?access_key=fa21cfc26f5ef926bd678abe21fb2b4f").json()
    data = req["rates"]
    lst = []
    lst2 = []
    for i in data:
        lst.append(i)
        lst2.append(req["rates"][f"{i}"])
    
    ziped = zip(lst,lst2)

    return render_template('home.html', data=ziped) 
@app.route('/crypto')
def crypto():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start':'1',
        'limit':'50',
        'convert':'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'd5fb6795-691a-4694-88b2-213cf6424b52',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data)
        kripto =  data["data"]
        naziv = []
        cena = []
        for  b in kripto:
            naziv.append(b["name"])
            cena.append(round((b["quote"]["USD"]["price"]), 2))
        
        ziped_crypto = zip(naziv,cena)

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return render_template('crypto.html', data = ziped_crypto )
@app.route('/register')
def register():
    return render_template('register.html')
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000 )
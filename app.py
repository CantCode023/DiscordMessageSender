from concurrent.futures import process
from flask import Flask, request, render_template
from mydiscord import Client

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/send")
def send():
    token = request.args['token']
    channelid = request.args['channelid']
    message = request.args['message']
    print(token,channelid,message)
    client = Client(str(token))

    try:
        a,b = client.sendMessage(channelid, message)
        return "Success"
    except Exception:
        return "There was an error when sending message."
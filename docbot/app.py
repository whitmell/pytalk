from flask import Flask, render_template, request

from docbot import *
from waitress import serve

bot = Bot('examples/const.txt')

app = Flask(__name__,static_url_path='/static')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/get")

def get_bot_response():
    userText = request.args.get('msg')
    if userText =='summary?':
      return bot.summary
    elif userText =='keywords?':
      return bot.keyphrases
    else :
      return bot.ask(userText)

if __name__ == "__main__":
  #app.run() # development only
  serve(app, host="0.0.0.0", port=8080) #production


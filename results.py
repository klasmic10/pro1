import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime, timedelta
from flask import Flask, render_template
import threading
import time

os.system("cls")
block = ""

# extract results
def checkresults():
    global block
    block = ""
    for count in range (-2,4):
        site = "https://www.sptulsian.com/f/result-calendar/results-on-"
        x = datetime.now() + timedelta(days=count)
        m = str(x.strftime("%b")).lower()
        w = x.strftime('%A') 
        block += w + ";"
        d = str(x.date())
        d = d.split("-")
        if int(d[2]) == 1:
            s = "st"
        elif int(d[2]) == 2:
            s = "nd"
        elif int(d[2]) == 3:
            s = "rd"
        else:
            s = "th"
        day = d[2] + s + "-" + m + "-" + d[0]
        block += day + ";"
        if count == 0:
            block += "TODAY" + ";"
        site += day
        r = requests.get(site)
        soup = BeautifulSoup(r.content, 'html.parser')
        try:
            d = soup.find(itemprop="description").get("content")
            d = d.split("below:")
            s = d[1].split("    ")
            c = 0
            for i in range (0,len(s)):
                s1 = s[i].split("  ")
                if len(s1) == 2:
                    t = s1[1]
                else:
                    t = s1[0]
                if len(t.split(" ")) == 3 and t.split(" ")[1] == "Cap":
                    t = t.upper()
                if t == "":
                    c += 1
                if c == 4:
                    break
                block += t + ";"
        except:
            pass
        block += "###"

# flask-server
app = Flask(__name__)
@app.route("/")
def home():
    return render_template('results.html')
@app.get("/update")
def update():
    return block
def server():
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)
threading.Thread(target=server).start()

while True:
    checkresults()
    time.sleep(300)







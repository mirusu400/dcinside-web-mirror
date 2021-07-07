#-*- coding:utf-8 -*-
import asyncio
import dc_api
import base64
import json
from core import *
from flask import Flask, render_template, request
from bs4 import BeautifulSoup,Tag

loop = asyncio.get_event_loop()
app = Flask(__name__)
gallerys=[]

@app.route("/")
def index():
    global gallerys
    global gallerys_miner_game
    global gallerys_miner_digital_it
    board = str(request.args.get("board", "None"))
    search = str(request.args.get("search", "None"))
    tgallerys = []
    sgallerys = None

    if "game" in board:
        sgallerys = gallerys_miner_game
    elif "digital" in board or "it" in board:
        sgallerys = gallerys_miner_digital_it
    else:
        sgallerys = gallerys

    if search != "None":
        for item in sgallerys:
            if search in item[0]:
                tgallerys.append(item)
    else:
        tgallerys = sgallerys
    return render_template('/index.html', gallerys=tgallerys)
        
# 공군갤 airforce
# 야갤 baseball_new10
# 싱벙갤 singlebungle1472
# 그림갤 drawing
@app.route('/board')
def board():
    # return "hi"
    page = int(request.args.get("page", 1))
    board = str(request.args.get("board", "airforce"))
    recommend = int(request.args.get("recommend",0))
    ret = loop.run_until_complete(async_index(page, board, recommend))
    return render_template('/board.html', datas=ret, page=page, board=board, recommend=recommend)

    
@app.route("/read")
def read():
    pid = int(request.args.get("pid", 0))
    board = str(request.args.get("board", "airforce"))
    data, comments, images = loop.run_until_complete(async_read(pid, board))
    # Parse soup, for image replation
    soup=BeautifulSoup(data["html"],'html.parser')
    idx = 0
    for i in soup.find_all("img", "lazy"):
        src = "data:image/png;base64," + images[idx]
        i["src"] = src
        idx += 1

    data["html"] = str(soup)
    return render_template('/read.html', data=data, comments=comments, images=images, board=board)



if __name__ == '__main__':
    with open("gallerys.json", "r", encoding="utf-8") as f:
        gallerys = list(json.load(f).items())
    with open("gallerys_miner_digital_it.json", "r", encoding="utf-8") as f:
        gallerys_miner_digital_it = list(json.load(f).items())
    with open("gallerys_miner_game.json", "r", encoding="utf-8") as f:
        gallerys_miner_game = list(json.load(f).items())

    app.run(debug=True, host="0.0.0.0", port=8080)
    
    


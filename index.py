#-*- coding:utf-8 -*-
import asyncio
import dc_api
import base64
import json
from core import *
from flask import Flask, render_template, request

loop = asyncio.get_event_loop()
app = Flask(__name__)
gallerys=[]

@app.route("/")
def index():
    global gallerys
    query = str(request.args.get("board", "None"))
    if query != "None":
        tgallerys=[]
        for item in gallerys:
            if query in item[0]:
                tgallerys.append(item)
        return render_template('/index.html', gallerys=tgallerys)
    else:
        return render_template('/index.html', gallerys=gallerys)
        
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
    return render_template('/read.html', data=data, comments=comments, images=images, board=board)



if __name__ == '__main__':
    with open("gallerys.json", "r", encoding="utf-8") as f:
        gallerys = list(json.load(f).items())

    app.run(debug=True, host="0.0.0.0", port=8080)
    
    


# -*- coding:utf8 -*-
import time
import MySQLdb
from flask import Flask, g, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from shark import *

tips = "查理歌词 v1.0\n请输入'歌曲名 歌手名'进行查找(中间是空格的说.)"
error_msg = "查理没用...查不到...\nbtw,您听歌的品味真独特.\n您确认格式正确?(歌名 歌手名)\n好啦还是人家太弱了啦...TAT"
  

app = Flask(__name__)

app.debug = True
from sae.const import (MYSQL_HOST, MYSQL_HOST_S, 
    MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
    )

@app.before_request
def before_request():
  g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS,
                        MYSQL_DB, port=int(MYSQL_PORT))

@app.teardown_request
def teardown_request(exception):
  if hasattr(g, 'db'): g.db.close()

@app.route('/', methods = ['GET', 'POST'] )
def wechat_auth():
  c = g.db.cursor()
  if request.method == 'GET':
    token = 'handalin'
    query = request.args
    signature = query.get('signature', '')
    timestamp = query.get('timestamp', '')
    nonce = query.get('nonce', '')
    echostr = query.get('echostr', '')
    s = [timestamp, nonce, token]
    s.sort()
    s = ''.join(s)
    if ( hashlib.sha1(s).hexdigest() == signature ):  
      return make_response(echostr)
  # Get the infomations from the recv_xml.
  xml_recv = ET.fromstring(request.data)
  ToUserName = xml_recv.find("ToUserName").text
  FromUserName = xml_recv.find("FromUserName").text
  Content = xml_recv.find("Content").text
  reply = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"

  if Content == 'h':
    Content = tips
  else:
    args = Content.split(' ')
    shark = SharkSearcher()
    try:
      for i in range(len(args)): args[i] = args[i].encode('utf8') # pass test
      Content = shark.feed( args )
      if Content == None : Content = error_msg
    except BaseException:
      Content = "HEHE"
  response = make_response( reply % (FromUserName, ToUserName, str(int(time.time())), Content ) )
  response.content_type = 'application/xml'
  return response



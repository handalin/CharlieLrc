# -*- coding:utf8 -*-
import urllib2, urllib
import sys
import re

class SharkSearcher():
  def __init__(self):
    pass

  def process_lrc(self, lrc):
    # rid of the beginning blank & replace the '<br />' with '\n'
    lrc = '\n'.join( lrc.strip().split('<br />') )
    return lrc
  
  def name_match(self, s, t):
    # check if s contain t.
    for ch in t:
      if s.find(t) == -1:
        return False
    return True

  def feed(self, args):
    myurl = 'http://www.xiami.com/search?key=' + '+'.join(args)
    # pretent to be IE. ^O^
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {}
    headers = { 'User-Agent':user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request(myurl, data, headers)
    try:
      html = urllib2.urlopen(req).read()
    except BaseException:
      return None
    song_urls = []
    try:
      pattern = r'<td class="song_name"><a target="_blank" href="([\s\S]+?)" title="([\s\S]+?)">[\s\S]+?</a></td>[\s\S]+?<td class="song_artist"><a target="_blank" href="/artist/.+?" title="([\s\S]+?)">[\s\S]+?</a></td>'
      result = re.findall( pattern, html)
      # 0 --- href ;    1 --- song name ;   2 --- artist name ;
      for i in range( len(result) ):
        if result[i][1].lower().find( args[0].lower() ) != -1 :
          if ( len(args) < 2 or self.name_match( result[i][2].lower(), args[1].lower() ) ):
            song_urls.append( result[i][0] )
            
    except BaseException:
      return None

    try:
      pattern = r'<div class="lrc_main">([\s\S]+?)</div>'
      req = urllib2.Request('http://www.xiami.com'+song_urls[0], data, headers)
      html = urllib2.urlopen(req).read()
      lrc = re.findall(pattern, html)[0]
    except BaseException:
      return None
    return self.process_lrc(lrc)

# -*- coding:utf8 -*-
import urllib2, urllib
import sys
import re

class SharkSearcher():
  def __init__():
    pass
  
  def process_lrc(self, lrc):
    return ''.join( lrc.split('<br />') )
  
  def feed(self, song, artist=None):
    myurl = 'http://www.xiami.com/search?key=' + song + '+' + artist
    
    # pretent to be IE. ^O^
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    values = {'name':'67',
        'location':'Northampton',
        'language':'Python'}
    headers = { 'User-Agent':user_agent}
    data = urllib.urlencode(values)
    req = urllib2.Request(myurl, data, headers)
    
    html = urllib2.urlopen(req).read()
    pattern = r'<td class="song_name"><a target="_blank" href="(.+)" title="'
    song_url = re.findall(pattern, html)[0]
    
    pattern = r'<div class="lrc_main">([\s\S]+?)</div>'
    req = urllib2.Request('http://www.xiami.com'+song_url, data, headers)
    html = urllib2.urlopen(req).read()
    lrc = re.findall(pattern, html)[0]
    
    return self.process_lrc(lrc)

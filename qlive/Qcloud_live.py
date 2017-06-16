#!/usr/bin/env python
import requests
import time
import hashlib
import sys
import json
import fire

class QQlive:
    def __init__(self):
        self.T = time.time()+600
        self.appid = 'xxxxxxx'
        self.apikey = 'xxxxxxx'
        self.url = 'http://fcgi.video.qcloud.com/common_access'

    def sign(self):
        myMd5 = hashlib.md5()
        myMd5.update(self.apikey+str(self.T))
        return myMd5.hexdigest()

    def channel_list(self):
        Li = []
        payload = {
                  't':self.T,
                  'sign':self.sign(),
                  'appid':self.appid,
                  'Param.n.order_type':1,
                  'interface':'Live_Channel_GetChannelList'
                  }
        body = requests.get(self.url, params=payload).json()
        for data in body['output']['channel_list']:
            channel_data = [ data['create_time'], data['channel_id'] ]
            Li.append(channel_data)
        return Li
            

    def geturl(self, ChannelID):
        Li = []
        payload = {'t':self.T,
                   'sign':self.sign(),
                   'appid':self.appid,
                   'interface':'Live_Tape_GetFilelist',
                   'Param.s.channel_id':ChannelID }
        body = requests.get(self.url, params=payload).json()
        for data in  body['output']['file_list']:
            mes = [ data['start_time'], data['end_time'], data['record_file_url'] ]
            Li.append(mes)
        return Li
        
if __name__ == '__main__':
    fire.Fire(QQlive)

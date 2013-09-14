# -*- coding: utf-8 -*-
import requests
import sys,os
from baidu.pcs import Client

class MyDataWrapper():
    def __init__(self):
        self.pcslist = {}
        self.initPCS()

    def initPCS(self):
        #first,  self.pcslist should be init with YOUR app name and access_token
        self.pcslist ={"PCS_APP_NAME1":"APP1_ACCESS_TOKEN","pcs_APP_NAME2":"APP2_ACCESS_TOKEN"}
        #print self.pcslist
        
    def pcsSearchBatch(self, keyword):
        searchResult = []
        for pcsname in self.pcslist:
            #print pcsname
            code, r = self.pcsSearch(pcsname, keyword)
            if(self.pcsCodeOK(code) and len(r['list'])>0):
                for itmInfo in r['list']:
                    searchResult.append(os.path.basename(itmInfo['path']))
                    #print os.path.basename(itmInfo['path'])
        return searchResult
        # demo return result:
        '''{
        "list":[
        {
        "fs_id":63313274,
        "path":"\/apps\/\u6d4b\u8bd5\u5e94\u7528\/\u6d4b\u8bd5\/pearlinux.txt",
        "ctime":1371998345,
        "mtime":1371998345,
        "md5":"b94ef70b058b4490bd2f647d35aa07db",
        "size":96,
        "isdir":0
        }
        ],
        "request_id":2870180983}'''

    def pcsSearch(self, pcsName, keyword):
        pcs = Client(self.pcslist[pcsName])
        try:
            code,r = pcs.search(self.APP_FOLDER(pcsName), keyword, re=1)
        except requests.exceptions.ConnectionError:
            print 'Network not connected.'
            print 'Exit.'
            exit()
        return code,r
        
    def pcsCodeOK(self, code):
        return (code == requests.codes.ok)
    
    def APP_FOLDER(self, pcsname):
        return "%s"%('/apps/'+pcsname+'/')

if __name__ == '__main__': 
    reload(sys)
    sys.setdefaultencoding('utf-8') 
    pcsclient = MyDataWrapper()
    #print sys.argv[1]
    for filename in pcsclient.pcsSearchBatch(sys.argv[1]):
        print filename.decode('utf-8')  #display chinese correctly, in win cmd.exe output.

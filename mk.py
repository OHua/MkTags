#!/usr/bin/env python
# coding:utf-8
import re


class MK :
    #__filepath = '.'
    #__encode='UTF-8'
    def __init__(self,filepath,encode='UTF-8'):
        self.filepath = filepath
        self.encode = encode
        self.mdfile = open(filepath,'r',encoding=encode).read()
        self.commenttags = []
        self.tags = []
        for comment in re.findall('<!--(.+)-->',self.mdfile) :
            self.commenttags += [{
                'comment':comment,
                'tags':self.findallTags(comment)
            }]
    def findallTags(self,contents):
        tags = list(map( (lambda x:x.strip()) ,re.findall('`([^`]+)`',contents)))
        self.tags += [ tag for tag in tags if tag not in self.tags ]
        return tags
    def listTags(self):
        return self.tags
    def matchTags(self,*tags):
        for tag in tags :
            print( tag , True if tag in self.tags else False )
    def addTags(self,*tags):
        newtags = [ tag for tag in tags if tag not in self.tags ]
        self.tags += newtags
        newcomments = [ '<!--`' + tag + '`-->' for tag in newtags ]

        f = open(self.filepath,'a' ,encoding = self.encode )
        f.write( '\n'.join(newcomments) )
        f.close()

        for tag in tags :
            print( tag , True if tag in newtags else False )
        #print( [tag+' : True' if tag in newtags else tag+' : False' for tag in tags] )
    def rmTags(self,*tags):
        rewrite = False
        for tag in tags :
            if tag in self.tags :
                for item in self.commenttags :
                    if tag in item['tags'] :
                        self.tags.remove(tag)
                        item['tags'].remove(tag)
                        newcomments = item['comment'].replace(tag,'')
                        self.mdfile = self.mdfile.replace(
                            item['comment'],
                            newcomments
                        )
                        item['comment'] = newcomments
                        print( tag , True )
                        rewrite = True
            else :
                print( tag , False )
        if rewrite :
            print('rewrite',rewrite)
            f = open(self.filepath,'w' ,encoding = self.encode )
            f.write(self.mdfile)
            f.close()

if __name__ == '__main__':
    m = MK('test.md')
    print(m.listTags())
    m.matchTags('python','ccc','abc')
    m.addTags('bb','bbb','bbbb')
# import datetime
# import timegm
# timestamp = int(os.environ.get('SOURCE_DATE_EPOCH', timegm(datetime.utcnow().utctimetuple())))
# timeobject = datetime.utcfromtimestamp(timestamp)

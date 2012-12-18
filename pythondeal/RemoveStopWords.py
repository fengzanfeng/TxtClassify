#!/user/bin/env python
# -*- coding: gb18030 -*-

import time
import re
import string
import os
import sys

class RemoveStopWords:
    def __init__(self,origin_F,des_F,stopWord_F,pattern):
        self.origin_F = origin_F
        self.des_F = des_F
        self.stopWord_F = stopWord_F
        self.pattern = pattern
        self.stopDict = {}
    def removeStopWords(self):
        pat = '[(' + self.pattern + ')(" ")(\n)(\r)(\r\n)]+'
        sep = ' '
        inClient = open(self.origin_F, 'rb')
        outClient = open(self.des_F, 'w')

        i = 0
        for line in inClient:
            i += 1
            try:
                gbline = unicode(line, 'utf-8', 'ignore')
                words = re.split(pat, gbline)
                afterRemove = []
                for word in words[1:]:
                    if not self.stopDict.has_key(word):
                        afterRemove.append(word)
                tmp = sep.join(afterRemove)
                tmp = words[0] + self.pattern + tmp
                outClient.write(tmp.encode('utf-8')+'\n')
            except:
                print 'error %s' % (i)
            if i % 100 == 0:
                sys.stdout.write("done: " + str(i) + "\r")
                sys.stdout.flush()
        inClient.close()
        outClient.close()
    
    def getStopWord(self):
        pat = '\r\n'
        inClient = open(self.stopWord_F,'rb')
        i = 0
        for line in inClient:
            line = re.split(pat,line)[0]
            i += 1
            try:
                gbline = unicode(line, 'gb18030', 'ignore')
                self.stopDict.setdefault(gbline, 0)
            except:
                print '%s : %s' % (line,i)
        print "stop words number: %s" % (i)
        inClient.close()

if __name__ == '__main__':
    start_time = time.clock()

    in_file = ''
    out_file = ''
    stop_word_file = ''
    pattern = '%%%%%%%%'
    length_of_para = len(sys.argv)
    if length_of_para % 2 != 1:
        print '参数个数错误'
        sys.exit()
    i = 1
    while i < length_of_para:
        if sys.argv[i][0] != '-':
            print '参数类别错误'
            sys.exit()
        if sys.argv[i][1] == 'i':
            in_file = sys.argv[i+1]
        elif sys.argv[i][1] == 's':
            out_file = sys.argv[i+1]
        elif sys.argv[i][1] == 'w':
            stop_word_file = sys.argv[i+1]
        i += 2
    rsw = RemoveStopWords(in_file, out_file, stop_word_file, pattern)
    rsw.getStopWord()
    rsw.removeStopWords()

    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

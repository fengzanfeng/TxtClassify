#!/user/bin/env python
# -*- coding: gb18030 -*-

import re
import sys
import string
import os
import math
import time
from math import *

class CreateVector:
    def __init__(self,in_file,out_file,IDF_file,pattern):
        self.in_F = in_file
        self.out_F = out_file
        self.IDF_F = IDF_file
        self.pattern = pattern
        self.ExtractFeature = {}
        self.docCount = {}
    def readIDF(self):
        pat = '[(" ")(\n)(\r)(\r\n)]+'
        inClient = open(self.IDF_F,'rb')
        i = 0
        for line in inClient:
            i += 1
            word,IDF,index,feature_weight = re.split(pat,line)[0:4]
            if not self.ExtractFeature.has_key(word):
                self.ExtractFeature[word] = [string.atof(IDF), string.atoi(index), feature_weight]
            else:
                print word
        inClient.close()
    
    def createVector(self):
        pat = '[(' + self.pattern + ')(" ")(\n)(\r)(\r\n)]+'
        inClient = open(self.in_F,'rb')
        outClient = open(self.out_F,'w')

        i = 0
        for line in inClient:
            i += 1
            words = re.split(pat, line)

            cate = words[0]
            self.docCount.setdefault(cate, 0)
            self.docCount[cate] += 1
            
            item_word_count = len(words[1:-1])
            item_dict = {}
            item_weight_dict = {}
            for word in words[1:-1]:
                item_dict.setdefault(word,0)
                item_dict[word] += 1
            for word in item_dict:
                if self.ExtractFeature.has_key(word):
                    index = self.ExtractFeature[word][1]
                    item_weight_dict.setdefault(index, 0)
                    TF = float(item_dict[word]) / item_word_count
                    IDF = self.ExtractFeature[word][0]
                    item_weight_dict[index] = TF * IDF * 10
            item_weight = sorted(item_weight_dict.iteritems(),key = lambda d:d[0])
            item_str = cate
            for item in item_weight:
                item_str += ' '
                item_str += str(item[0])
                item_str += ':'
                item_str += str(item[1])
            outClient.write(item_str + '\n')
        inClient.close()
        outClient.close()
    def printDocInfo(self):
        for key in self.docCount:
            print key, self.docCount[key]
if __name__ == '__main__':
    start_time = time.clock()

    in_file = ''
    out_file = ''
    IDF_file = ''
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
        elif sys.argv[i][1] == 'f':
            IDF_file = sys.argv[i+1]
        i += 2
    cv = CreateVector(in_file,out_file,IDF_file,pattern)
    cv.readIDF()
    cv.createVector()
    cv.printDocInfo()
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

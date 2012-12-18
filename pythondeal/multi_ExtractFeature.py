#!/usr/bin/env python
# -*- coding: gb18030 -*-

import time
import re
import string
import os
import math
import sys
from math import *

class multi_ExtractFeature:
    def __init__(self, in_file, out_file, sep, number):
        self.in_F = in_file
        self.out_F = out_file
        self.sep = sep
        self.num = number

        self.docCount = {}
        self.wordCount = {}
        self.Feature = {}
    def countABCD(self):
        reg = '[(' + self.sep + ')(" ")(\n)(\t)(\r)(\r\n)]+'
        inClient = open(self.in_F,'rb')
        i = 0
        for line in inClient:
            i += 1
            try:
                words = re.split(reg,line)
                cate = string.atoi(words[0])
                self.docCount.setdefault(cate, 0)
                self.docCount[cate] += 1

                wd_count = {} #统计每个文档中每个词的频数的变量word doc count
                for word in words[1:-1]:
                    wd_count.setdefault(word, 0)
                    wd_count[word] += 1
                for word in wd_count:
                    self.wordCount.setdefault(word, {})
                    self.wordCount[word].setdefault(cate, [0, 0])
                    self.wordCount[word][cate][0] += 1
                    self.wordCount[word][cate][1] += wd_count[word]
            except Exception,e:
                print '%s in %s' % (e,i)
        inClient.close()
        print 'word count all is %s ' % (len(self.wordCount))
    
    def calCHI(self):
        catekeys = self.docCount.keys()
        AllDoc = 0 #所有的文档数目
        for cate in catekeys:
            AllDoc += self.docCount[cate]
        i = 0
        for word in self.wordCount:
            i += 1
            AllWordDoc = 0 #出现word的所有文档数目
            for cate in catekeys:
                AllWordDoc += self.wordCount[word].get(cate,[0,0])[0]
            CHIList = {}
            for cate in catekeys:
                A = float(self.wordCount[word].get(cate,[0,0])[0])
                C = float(self.docCount[cate] - A)
                B = float(AllWordDoc - A)
                D = float(AllDoc - self.docCount[cate] - B)
                CHI = ((A*D - B*C)**2)/((A+B) * (C+D))
                CHIList[cate] = CHI
            CHI = max(CHIList.items(),key = lambda x:x[1])[1]
            IDF = log(float(AllDoc)/AllWordDoc)
            self.Feature.setdefault(word,[0.0,0.0,{}])
            self.Feature[word][0] = CHI
            self.Feature[word][1] = IDF
            self.Feature[word][2] = CHIList

    def calMI(self):
        catekeys = self.docCount.keys()
        AllDoc = 0
        for cate in catekeys:
            AllDoc += self.docCount[cate]
        i = 0
        for word in self.wordCount:
            i += 1
            AllWordDoc = 0
            for cate in catekeys:
                AllWordDoc += self.wordCount[word].get(cate,[0,0])[0]
            MIList = {}
            for cate in catekeys:
                A = float(self.wordCount[word].get(cate,[0,0])[0])
                C = float(self.docCount[cate] - A)
                B = float(AllWordDoc - A)
                mi = A * AllDoc / ((A+C)*(A+B))
                if mi == 0:
                    MI = 0.0
                else:
                    MI = fabs(log(mi))
                MIList[cate] = MI
            MI = max(MIList.items(),key = lambda x:x[1])[1]
            IDF = log(float(AllDoc)/AllWordDoc)
            self.Feature.setdefault(word,[0.0,0.0,{}])
            self.Feature[word][0] = MI
            self.Feature[word][1] = IDF
            self.Feature[word][2] = MIList
    
    def calIG(self):
        catekeys = self.docCount.keys()
        AllDoc = 0
        SumPCI = 0.0
        for cate in catekeys:
            AllDoc += self.docCount[cate]
        for cate in catekeys:
            pci = self.docCount[cate]/float(AllDoc)
            PCI = pci * log(pci)
            SumPCI -= PCI
        i = 0
        for word in self.wordCount:
            i += 1
            AllWordDoc = 0
            for cate in catekeys:
                AllWordDoc += self.wordCount[word].get(cate,[0,0])[0]
            NoWordDoc = AllDoc - AllWordDoc
            PT = float(AllWordDoc) / AllDoc
            P_T = float(NoWordDoc) / AllDoc
            SumPCIT = 0.0
            SumPCI_T = 0.0
            for cate in catekeys:
                cword = self.wordCount[word].get(cate,[0,0])[0]
                pcit = cword / float(AllWordDoc)
                pci_t = (self.docCount[cate] - cword) / float(NoWordDoc)
                if pcit == 0:
                    PCIT = 0
                else:
                    PCIT = pcit * log(pcit)
                if pci_t == 0:
                    PCI_T = 0
                else:
                    PCI_T = pci_t * log(pci_t)
                SumPCIT += PCIT
                SumPCI_T += PCI_T
            IG = SumPCI + PT * SumPCIT + P_T * SumPCI_T
            IDF = log( float(AllDoc) / AllWordDoc )
            self.Feature.setdefault(word,[0.0,0.0,{}])
            self.Feature[word][0] = IG
            self.Feature[word][1] = IDF

    def calDD(self):
        catekeys = self.docCount.keys()
        AllDoc = 0 #所有的文档数目
        for cate in catekeys:
            AllDoc += self.docCount[cate]
        i = 0
        for word in self.wordCount:
            i += 1
            AllWordDoc = 0 #出现word的所有文档数目
            for cate in catekeys:
                AllWordDoc += self.wordCount[word].get(cate,[0,0])[0]

            DDList = {}
            for cate in catekeys:
                wordDoc = float(self.wordCount[word].get(cate,[0,0])[0])
                cateDoc = float(self.docCount.get(cate,1))
                DD = wordDoc / cateDoc
                DDList.setdefault(cate,0.0)
                DDList[cate] = DD
            DDmax = max(DDList.items(),key = lambda x:x[1])[1]
            DDmin = min(DDList.items(),key = lambda x:x[1])[1]
            IDF = log(float(AllDoc)/AllWordDoc)
            DD = DDmax - DDmin
            self.Feature.setdefault(word,[0.0,0.0,{}])
            self.Feature[word][0] = DD
            self.Feature[word][1] = IDF
            self.Feature[word][2] = DDList
    
    def sortFeature(self):
        self.FeatureSorted = sorted(self.Feature.iteritems(),key = lambda d:d[1][0],reverse = True)
    
    def writeToFile(self):
        outClient = open(self.out_F,'w')
        i = 0
        for item in self.FeatureSorted[0:self.num]:
            i += 1
            string = item[0] + ' ' + str(item[1][1]) + ' ' + str(i) + ' ' + str(item[1][0]) + '\n'
            outClient.write(string)
        outClient.close()

if __name__ == '__main__':
    start_time = time.clock()

    in_file = ''
    out_file = ''
    sep = '%%%%%%%%'
    number = 25000

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
        elif sys.argv[i][1] == 'n':
            number = string.atoi(sys.argv[i+1])
        i += 2

    mef = multi_ExtractFeature(in_file, out_file, sep, number)
    
    sys.stdout.write("couting ......\r")
    sys.stdout.flush()
    
    mef.countABCD()
    
    sys.stdout.write("calculating ......\r")
    sys.stdout.flush()
    
    mef.calCHI()
    #mef.calDD()
    #mef.calMI()
    #mef.calIG()
    
    sys.stdout.write("sorting ......\r")
    sys.stdout.flush()
    
    mef.sortFeature()
    
    sys.stdout.write("writing ......\r")
    sys.stdout.flush()
    
    mef.writeToFile()
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

#!/usr/bin/env python
# -*- coding: gb18030 -*-

import re
import sys
import string
import os
import math
import time
from math import *

class NavieBayesTrain:
    def __init__(self, removed_file, model_file, sep):
        self.removed_F = removed_file
        self.model_F = model_file
        self.sep = sep
        self.docCount = {}
        self.wordCount = {}
    
    def countVar(self, features):
        reg = '[(' + self.sep + ')(" ")(\n)(\t)(\r)(\r\n)]+'
        inClient = open(self.removed_F, 'rb')
        i = 0
        for line in inClient:
            i += 1
            words = re.split(reg, line)
            cate = words[0]
            self.docCount.setdefault(cate, 0)
            self.docCount[cate] += 1

            wd_count = {} #统计每个文档中的词频，防止计数时每个词出现的文档数和每个词的词频数混淆
            for word in words[1:-1]:
                if features.has_key(word):
                    wd_count.setdefault(word, 0)
                    wd_count[word] += 1
            for word in wd_count:
                self.wordCount.setdefault(word, {})
                self.wordCount[word].setdefault(cate, [0,0])
                self.wordCount[word][cate][0] += 1
                self.wordCount[word][cate][1] += wd_count[word]
        inClient.close()
        print 'word count all is %s' % (len(self.wordCount))
        print 'cate count all is %s' % (len(self.docCount))
    
    def trainPolynomialModel(self):
        catekeys = self.docCount.keys()
        vacabulary = len(self.wordCount)
        words_of_cate = {}
        AllWord = 0
        for cate in catekeys:
            words_of_cate.setdefault(cate, 0)
            for word in self.wordCount:
                words_of_cate[cate] += self.wordCount[word].get(cate, [0,0])[1]
        for cate in catekeys:
            AllWord += words_of_cate[cate]
        self.prior_prob = {}
        self.condition_prob = {}
        for cate in catekeys:
            self.prior_prob.setdefault(cate, 0.0)
            self.prior_prob[cate] = words_of_cate[cate] / float(AllWord)
        for word in self.wordCount:
            self.condition_prob.setdefault(word, {})
            for cate in catekeys:
                self.condition_prob[word].setdefault(cate, 0.0)
                con_prob = (self.wordCount[word].get(cate, [0,0])[1] + 1.0) / float(words_of_cate[cate] + vacabulary)
                self.condition_prob[word][cate] = con_prob
    
    def writeToModel(self):
        outClient = open(self.model_F,'w')
        cates = len(self.prior_prob)
        words = len(self.condition_prob)
        catekeys = self.prior_prob.keys()
        outClient.write('cates:' + str(cates) + '\n')
        outClient.write('words:' + str(words) + '\n')
        for cate in catekeys:
            outClient.write(cate + ':' + str(self.prior_prob[cate]) + '\n')
        for word in self.condition_prob:
            outClient.write(word)
            for cate in catekeys:
                outClient.write(' ' + cate + ':' + str(self.condition_prob[word][cate]))
            outClient.write('\n')
        outClient.close()

class Feature:
    def __init__(self,feature_file):
        self.feature_F = feature_file
        self.Features = {}
    def readFeatures(self):
        pat = '[(" ")(\n)(\r)(\t)]+'
        inClient = open(self.feature_F,'rb')
        i = 0
        for line in inClient:
            i += 1
            word,IDF = re.split(pat,line)[0:2]
            if not self.Features.has_key(word):
                self.Features[word] = string.atof(IDF)
            else:
                print word
        inClient.close()
        print len(self.Features)
    def GetFeatures(self):
        if len(self.Features) == 0:
            self.readFeatures()
        return self.Features


if __name__ == '__main__':
    start_time = time.clock()

    removed_file = ''
    feature_file = ''
    model_file = ''
    sep = '%%%%%%%%'
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
            removed_file = sys.argv[i+1]
        elif sys.argv[i][1] == 'f':
            feature_file = sys.argv[i+1]
        elif sys.argv[i][1] == 'm':
            model_file = sys.argv[i+1]
        i += 2

    f = Feature(feature_file)
    print 'Geting features ...'
    features = f.GetFeatures()
    nbt = NavieBayesTrain(removed_file, model_file, sep)
    print 'counting variables ...'
    nbt.countVar(features)
    print 'training models ...'
    nbt.trainPolynomialModel()
    print 'writing to model file ...'
    nbt.writeToModel()
    
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

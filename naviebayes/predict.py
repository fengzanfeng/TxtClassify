#!/usr/env/python
# -*- coding: gb18030 -*-

import re
import string
import sys
import os
import math
import time
from math import *

class NavieBayesPredict:
    def __init__(self,removed_file,model_file,predict_file,sep):
        self.removed_F = removed_file
        self.model_F = model_file
        self.predict_F = predict_file
        self.sep = sep
        self.prior_prob = {}
        self.condition_prob = {}

    def __calLogForCondition(self):
        log_prob ={}
        catekeys = self.prior_prob.keys()
        for word in self.condition_prob:
            log_prob.setdefault(word,{})
            for cate in catekeys:
                log_prob[word].setdefault(cate,[0.0,0.0])
                log_prob[word][cate][0] = log(self.condition_prob[word][cate])
                log_prob[word][cate][1] = log(1.0 - self.condition_prob[word][cate])
        return log_prob
    
    def predictPolynomial(self, features):
        reg = '[(' + self.sep + ')(" ")(\n)(\t)(\r)(\r\n)]+'
        inClient = open(self.removed_F,'rb')
        outClient = open(self.predict_F,'w')
        right_predict = 0
        i = 0
        for line in inClient:
            i += 1
            words = re.split(reg,line)
            wd_count = {} #统计每个文档中出现在特征集中的单词词频，现在没用到词频，只用到单词是否出现的信息
            item_word_count = len(words[1:-1]) #TF之分母
            for word in words[1:-1]:
                if features.has_key(word):
                    wd_count.setdefault(word,0)
                    wd_count[word] += 1
            predict_prob = {}
            catekeys = self.prior_prob.keys()
            for cate in catekeys:
                predict_prob[cate] = log(self.prior_prob[cate])
            for cate in catekeys:
                for word in wd_count:
                    if self.condition_prob.has_key(word):
                        TF = wd_count[word]
                        IDF = features[word]
                        predict_prob[cate] += TF * log(self.condition_prob[word][cate])
                    else:
                        print 'error on word %s' % (word)
            predict_cate = max(predict_prob.items(),key = lambda x:x[1])[0]
            cate = words[0]
            if cate == predict_cate:
                right_predict += 1
            outClient.write(predict_cate + '\n')
        inClient.close()
        outClient.close()
        print 'right_predict/allDoc = %s / %s , Accuracy is %s' %(right_predict,i,float(right_predict)/i)
    
    def readModel(self):
        inClient = open(self.model_F,'rb')
        catesline = inClient.readline()[0:-1]
        wordsline = inClient.readline()[0:-1]
        catesNum = int(catesline[catesline.find(':')+1:])
        wordsNum = int(wordsline[wordsline.find(':')+1:])
        i = 0
        while i < catesNum:
            i += 1
            cateline = inClient.readline()[0:-1]
            pos = cateline.find(':')
            cate = cateline[0:pos]
            prob = float(cateline[pos+1:])
            self.prior_prob.setdefault(cate, 0.0)
            self.prior_prob[cate] = prob
        i = 0
        while i < wordsNum:
            i += 1
            wordline = inClient.readline()[0:-1]
            infolist = wordline.split(' ')
            word = infolist[0]
            self.condition_prob.setdefault(word, {})
            for info in infolist[1:]:
                pos = info.find(':')
                cate = info[0:pos]
                prob = float(info[pos+1:])
                self.condition_prob[word].setdefault(cate, 0.0)
                self.condition_prob[word][cate] = prob
        inClient.close()

class Feature:
    def __init__(self,feature_file):
        self.feature_F = feature_file
        self.Features = {}
    def readFeatures(self):
        pat = '[(" ")(\n)(\r)(\t)(\r\n)]+'
        inClient = open(self.feature_F, 'rb')
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
    predict_file = ''
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
        elif sys.argv[i][1] == 's':
            predict_file = sys.argv[i+1]
        i += 2

    f = Feature(feature_file)
    print 'Getting features ...'
    features = f.GetFeatures()
    nbp = NavieBayesPredict(removed_file,model_file,predict_file,sep)
    print 'reading models ...'
    nbp.readModel()
    print 'predicting testset ...'
    nbp.predictPolynomial(features)
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

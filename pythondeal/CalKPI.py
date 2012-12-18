#!/user/bin/env python
# -*- coding: gb18030 -*-

import time
import re
import string
import math
import os
import sys

class CalKPI:
    def __init__(self,testfile,predict,pattern):
        self.test_F = testfile
        self.predict_F = predict
        self.pattern = pattern
    
    def calAllKPI(self):
        inClient1 = open(self.test_F,'rb')
        inClient2 = open(self.predict_F,'rb')
        i = 0
        self.result = {}
        for (rightline,predictline) in zip(inClient1,inClient2):
            i += 1
            right = rightline.split(self.pattern)[0]
            predict = re.sub('[(\r)(\n)(\t)(" ")(\r\n)]+','',predictline)
            self.result.setdefault(right,{})
            self.result.setdefault(predict,{})
            if right == predict:
                self.result[right].setdefault('a',0)
                self.result[right]['a'] += 1
            else:
                self.result[right].setdefault('c',0)
                self.result[right]['c'] += 1
                self.result[predict].setdefault('b',0)
                self.result[predict]['b'] += 1
            self.result[right].setdefault('all',0)
            self.result[right]['all'] += 1
        print '微平均(正确率，召回率，F1):'
        rightNum = 0
        allNum = 0
        for cate in self.result:
            print '%s类： 判定正确/总数： %s/%s = %s' % (cate, self.result[cate]['a'], self.result[cate]['all'], float(self.result[cate]['a'])/self.result[cate]['all'])
            rightNum += self.result[cate]['a']
            allNum += self.result[cate]['all']
        print 'All 判定正确/总数: %s/%s = %s' % (rightNum, allNum, float(rightNum)/allNum)
        print '\n宏平均：'
        P = 0.0
        R = 0.0
        F1 = 0.0
        for cate in self.result:
            a = self.result[cate]['a']
            b = self.result[cate]['b']
            c = self.result[cate]['c']
            a_b = a + b
            a_c = a + c
            precision = a / float(a_b)
            recall = a / float(a_c)
            f1 = 2 * precision * recall / ( precision + recall)
            print 'cate:%s\t precision: %s/%s = %s\t recall: %s/%s = %s\t F1:%s' % (cate,a,a_b,precision,a,a_c,recall,f1)
            P += precision
            R += recall
            F1 += f1
        cateNum = float(len(self.result))
        print 'P:%s\t R:%s\t F1:%s' % ( P/cateNum, R/cateNum, F1/cateNum)
        inClient1.close()
        inClient2.close()

if __name__ == '__main__':
    start_time = time.clock()
    test_file = ''
    predict_file = ''
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
        if sys.argv[i][1] == 'p':
            predict_file = sys.argv[i+1]
        elif sys.argv[i][1] == 't':
            test_file = sys.argv[i+1]
        i += 2
    cal = CalKPI(test_file,predict_file,pattern)
    cal.calAllKPI()
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

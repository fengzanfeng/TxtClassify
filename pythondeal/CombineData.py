#!/usr/bin/env python
# -*- coding: gb18030 -*-

import os
import string
import sys
import re
import time

class FileCombiner:
    def __init__(self, src_path, des_file):
        self.src_path = src_path
        self.des_file = des_file
        self.list_file = {}
        self.sep = '%%%%%%%%'
    def getListPath(self):
        root_list = os.listdir(self.src_path)
        for folder in root_list:
            son_path = self.src_path + '/' + folder
            if not os.path.isdir(son_path):
                continue
            file_list = os.listdir(son_path)
            self.list_file.setdefault(folder,[])
            for filename in file_list:
                file_path = son_path + '/' + filename
                self.list_file[folder].append(file_path)
    def combine(self):
        reg = '[(\t)(\n)(\r)(" ")("　")]+'
        outClient = open(self.des_file,'w')
        no_use_cate = []
        i = 0
        for key in self.list_file:
            cate = key[1:key.find('-')]
            if len(self.list_file[key]) < 200:
                no_use_cate.append(key)
                continue
            for file_path in self.list_file[key]:
                if os.path.isfile(file_path):
                    inClient = open(file_path,'r')
                    content = inClient.read()
                    content = unicode(content,'gb18030','ignore')
                    content = re.sub(unicode(reg,'gb18030'),' ',content)
                    outClient.write(cate + self.sep + content.encode('utf-8') + '\n')
                    inClient.close()
                    i += 1
                    if i % 100 == 0:
                        sys.stdout.write("done: " + str(i) + "\r")
                        sys.stdout.flush()
        outClient.close()
        self.printCombineInfo(no_use_cate)

    def printCombineInfo(self, no_use_cate):
        i = 0
        print 'all keys:'
        for key in self.list_file:
            if key not in no_use_cate:
                print key, len(self.list_file[key])
                i += len(self.list_file[key])
        print 'all chosed files: ', i
        print '\nno_use_cate:'
        for key in no_use_cate:
            print key, len(self.list_file[key])
if __name__ == '__main__':
    start_time = time.clock()

    src_path = ''
    des_file = ''
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
            src_path = sys.argv[i+1]
        elif sys.argv[i][1] == 's':
            des_file = sys.argv[i+1]
        i += 2
    fc = FileCombiner(src_path, des_file)
    fc.getListPath()
    fc.combine()
    end_time = time.clock()
    print 'time used : %s s' % (end_time - start_time)

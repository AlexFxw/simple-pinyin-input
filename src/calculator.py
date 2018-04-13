from file_loader import Analyzer
import re
from pypinyin import lazy_pinyin
import math
import sys

input_path = '../data/input的副本.txt'
output_path = '../data/output.txt'
c_num = 20
alpha = 0.01 
beta = 1 - alpha
min_num = 0

class node:
    def __init__(self):
        self.s = '' 
        self.f = 0.0

class Calculator:
    def __init__(self,a):
        self.analyzer = a
        self.pb_dict = {} 
        self.pinyin = []
        self.ans_sentence = {}
        self.ans_dict = {}
    def read_in(self, path):
        with open (path, 'r') as f:
            for line in f.readlines():
                cur_str = re.sub('\n', '', line)
                self.pinyin.append(re.split(' ', cur_str))
    def viterbi(self):
        for py_list in self.pinyin:
            l = len(py_list)
            self.pb_dict = {} 
            self.ans_sentence = {}
            self.ans_dict = {}
            for i in range(1, l):
                py = py_list[i-1].lower() + ' ' + py_list[i].lower()
                cur_list = self.analyzer.find_choice(py_list[i].lower(), 1)
                last_list = self.analyzer.find_choice(py_list[i-1].lower(), 1)
                pair_list = self.analyzer.find_choice(py, 2)
                tmp_dict = {}
                for cur in cur_list:
                    cur = cur[0]
                    tmp_dict[cur] = {}
                    for item in last_list:
                        last = item[0]
                        tmp_dict[cur][last] = min_num 
                        pair_cnt = self.sum(last+cur, pair_list) 
                        p = self.trans_pbty(last,cur,last_list,cur_list,pair_list)
                        if i == 1:
                            tmp_dict[cur][last] = alpha * p * item[1]/self.analyzer.single_num 
                        else:
                            for j in self.pb_dict[i-1][last].keys():
                                f = self.pb_dict[i-1][last][j] * p 
                                if f > tmp_dict[cur][last]:
                                    tmp_dict[cur][last] = f
                self.pb_dict[i] = tmp_dict
            ans_list = []
            self.ans_dict = {}
            for cur in self.pb_dict[l-1].keys():
                ans_list.append(self.find_ans(l-1, cur))
            ans_nd = node()
            ans_nd.f = min_num 
            for item in ans_list:
                if item.f > ans_nd.f:
                    ans_nd = item
            print(py_list)
            print(ans_nd.s)
    def find_ans(self, i, cur):
        if i not in self.ans_dict.keys():
            self.ans_dict[i] = {}
        if cur not in self.ans_dict[i].keys():
            nd = node()
            if i == 0:
                nd.f = 1.0
                nd.s = ''
            else:
                nd.f = min_num 
                for item in self.pb_dict[i][cur].keys():
                    n = self.find_ans(i-1,item)
                    p = self.pb_dict[i][cur][item] * n.f
                    if p > nd.f:
                        nd.f = p
                        if i == 1:
                            nd.s = item + cur
                        else:
                            nd.s = n.s + cur 
            self.ans_dict[i][cur] = nd
        #print(self.ans_dict[i][cur].s)
        return self.ans_dict[i][cur]
    def sum(self, word, word_list):
        for item in word_list:
            if word == item[0]:
                return item[1]
        return 0
    def trans_pbty(self, last, cur, last_list, cur_list, pair_list):
        cur_cnt = self.sum(cur, cur_list)
        last_cnt = self.sum(last, last_list)
        pair_cnt = self.sum(last+cur, pair_list)
        if last_cnt == 0 or pair_cnt == 0:
            return alpha*cur_cnt/self.analyzer.single_num
        else:
            return alpha*(cur_cnt/self.analyzer.single_num) + beta*(pair_cnt / last_cnt) 
        
a = Analyzer()
a.load()
c = Calculator(a)
c.read_in(input_path)
c.viterbi()

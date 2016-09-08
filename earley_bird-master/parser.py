#!/usr/bin/python
# coding=utf-8
# -*- encoding: utf-8 -*-

from chart import *
from grammar import *

# 定义Parser
class Parser:
    GAMMA_SYMBOL = 'GAMMA'

    def __init__(self, grammar, sentence, debug=False):
        '''Initialize parser with grammar and sentence
            输入： 语法集；句子；debug标记
        '''
        self.grammar = grammar
        self.sentence = sentence
        self.debug = debug

        # prepare a chart for every input word
        self.charts = [Chart([]) for i in range(len(self)+1)]           # 假设输入token是n个，则charts是n+1个元素.
        self.complete_parses = []           # 已完成的parses被做成列表, 列表中装载的是ChartRow对象(earley item).

    def __len__(self):
        '''Length of input sentence'''
        return len(self.sentence)

    def init_first_chart(self):
        '''Add initial Gamma rule to first chart'''
        row = ChartRow(Rule(Parser.GAMMA_SYMBOL, ['S']), 0, 0)
        # 调用ChartRow class的初始化方法，新建一个chart row. 
        # 初始化的参数，第一个是被格式化的rule, dot和start都是0.
        self.charts[0].add_row(row)
        # 添加row

    def prescan(self, chart, position):
        '''Scan current word in sentence, and add appropriate
           grammar categories to current chart'''
        word = self.sentence[position-1]
        if word:
            rules = [Rule(tag, [word.word]) for tag in word.tags]
            for rule in rules:
                chart.add_row(ChartRow(rule, 1, position-1))

    def predict(self, chart, position):
        '''Predict next parse by looking up grammar rules
           for pending categories in current chart'''
        for row in chart.rows:
            next_cat = row.next_category()
            rules = self.grammar[next_cat]
            if rules:
                for rule in rules:
                    new = ChartRow(rule, 0, position)
                    chart.add_row(new)

    def complete(self, chart, position):
        '''Complete a rule that was done parsing, and
           promote previously pending rules'''
        for row in chart.rows:    # 扫描当前chart的每一个earley state
            if row.is_complete():
                completed = row.rule.lhs
                for r in self.charts[row.start].rows:
                    if completed == r.next_category():
                        new = ChartRow(r.rule, r.dot+1, r.start, r, row)
                        chart.add_row(new)

    def parse(self):
        '''Main Earley's Parser loop'''
        self.init_first_chart()

        i = 0
        # we go word by word
        while i < len(self.charts):
            chart = self.charts[i]
            self.prescan(chart, i) # scan current input

            # predict & complete loop
            # rinse & repeat until chart stops changing
            length = len(chart)
            old_length = -1
            while old_length != length:
                self.predict(chart, i)
                self.complete(chart, i)

                old_length = length
                length = len(chart)

            i+= 1

        # finally, print charts for debuggers
        if self.debug:
            print "Parsing charts:"
            for i in range(len(self.charts)):
                print "-----------{0}-------------".format(i)
                print self.charts[i]
                print "-------------------------".format(i)

    def is_valid_sentence(self):
        '''Returns true if sentence has a complete parse tree'''
        res = False
        for row in self.charts[-1].rows:
            if row.start == 0:
                if row.rule.lhs == self.GAMMA_SYMBOL:
                    if row.is_complete():
                        self.complete_parses.append(row)
                        res = True
        return res


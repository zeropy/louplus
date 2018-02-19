#!/usr/bin/env python
# coding=utf-8

'''
    Usage: python calculator.py -c test.cfg -d user.csv -o gongzi.csv
    Option:
        -c test.cfg 配置文件
        -d user.csv 原始工资数据
        -o gongzi.csv 税后工资数据
'''

import sys
import os
import getopt
import csv
from collections import namedtuple
from multiprocessing import Process,Queue
import queue


class Args(object):
    def __init__(self):
        self.conf, self.userdata, self.resfile = self._parser_args()

    def _parser_args(self):
        conf = None
        userdata = None
        resfile = None

        try:
            opts,args = getopt.getopt(sys.argv[1:],'c:d:o:')
        except IndexError as e:
            print('Parameter Error')

        for opt,arg in opts:
            if opt == '-c':
                conf = arg
            elif opt == '-d':
                userdata = arg
            elif opt == '-o':
                resfile = arg
        return conf,userdata,resfile

class Config(object):
    def __init__(self,conf):
        self.JiShuH, self.JiShuL, self.scioal_insurance_rate = self._parse_config(conf)

    def _parse_config(self,conf):
        with open(conf,'r') as f:
            scioal_insurance_rate = 0
            for line in f:
                line = line.strip().split()
                opt = line[0]
                arg = line[2]
                if opt == 'JiShuH':
                    JiShuH = float(arg)
                elif opt == 'JiShuL':
                    JiShuL = float(arg)
                else:
                    scioal_insurance_rate += float(arg)
        return JiShuH,JiShuL,scioal_insurance_rate

class Employee(object):
    def __init__(self,datafile):
        self.datafile = datafile

    def load_userdata_perline(self,datafile):
        with open(datafile,'r') as f:
            spamreader = csv.reader(f,delimiter=',')
            for row in spamreader:
                job_number = int(row[0])
                salay = int(row[1])
                yield job_number,salay

    def __iter__(self):
        return self.load_userdata_perline(self.datafile)

class Calculator(object):
    START_TAX_POINT = 3500
    tax_table =  namedtuple('tax_table',['taxable_part','tax_rate','deduction'])
    tax_list = [
      tax_table(80000,0.45,13500),
      tax_table(55000,0.35,5505),
      tax_table(35000,0.30,2755),
      tax_table(9000,0.25,1005),
      tax_table(4500,0.20,555),
      tax_table(1500,0.10,105),
      tax_table(0,0.03,0),
    ]

    def __init__(self,config,number,salay):
        self.config = config
        self.number = number
        self.salay = salay

    def calc_scioal_insurance(self,config,salay):
        if salay >= config.JiShuH:
            salay_of_insurance = config.JiShuH
        elif salay <= config.JiShuL:
            salay_of_insurance = config.JiShuL
        else:
            salay_of_insurance = salay

        insurance_money = salay_of_insurance * config.scioal_insurance_rate
        return insurance_money

    def calc_tax(self,config,income):
        taxable_part = income - self.START_TAX_POINT
        if taxable_part <= 0:
            return income,0
        for t in self.tax_list:
            if taxable_part > t.taxable_part:
                tax = taxable_part * t.tax_rate - t.deduction
                real_income = income - tax
                return real_income, tax

    def calc_all(self,config,salay):
        insurance_money = self.calc_scioal_insurance(config,salay)
        income = self.salay - insurance_money
        real_income,tax = self.calc_tax(config,income)
        return self.number,self.salay,insurance_money,tax,real_income




class Export(object):
    def __init__(self,outfile):
        self._file = open(outfile,'w')

    def close(self):
        self._file.close()

    def writer(self,t):
        line = '{:d}, {:d}, {:.2f}, {:.2f}, {:.2f}\n'.format(*t)
        self._file.write(line)

class Execute(object):
    def __init__(self):
        a = Args()
        self.config = Config(a.conf)
        self.employee_data = Employee(a.userdata)
        self.outfile = a.resfile

    def _load_employee(self,q):
        for t in self.employee_data:
            q.put(t)

    def _calc(self,read_q,output_q):
        while True:
            try:
                num,salay = read_q.get(timeout=1)
            except queue.Empty as e:
                break
            c = Calculator(self.config,num,salay)
            t = c.calc_all(self.config,salay)

            output_q.put(t)

    def _exporter(self,q):
        e = Export(self.outfile)
        while True:
            try:
                t = q.get(timeout=1)
            except queue.Empty as e:
                break
            e.writer(t)

    def excute(self):
        q1 = Queue()
        q2 = Queue()
        p1 = Process(target=self._load_employee,args=(q1,))
        p2 = Process(target=self._calc,args=(q1,q2,))
        p3 = Process(target=self._exporter,args=(q2,))
        p1.start()
        p2.start()
        p3.start()
        p1.join()
        p2.join()
        p2.join()

if __name__ == '__main__':
    #a = Args()
    #c = Config(a.conf)
    #e = Employee(a.userdata)
    #expoter = Export(a.resfile)
    #for num,salay in e:
    #    calc = Calculator(c,num,salay)
    #    t = calc.calc_all(c,salay)
    #    expoter.writer(t)
    #expoter.close()
    e = Execute()
    e.excute()



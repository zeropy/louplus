#!/usr/bin/env python
# coding=utf-8

import sys
import os
from collections import namedtuple
import csv



class Config(object):
    def __init__(self,conf):
        self.JiShuH = 0
        self.JiShuL = 0
        self.scioal_insurance_rate = self._scioal_insurance_rate(conf)

    def _scioal_insurance_rate(self,conf):
        scioal_insurance_type = ['YangLao','YiLao','GongShang','ShiYe','ShengYu','GongJiJin']
        scioal_insurance_rate = 0
        with open(conf,'r') as f:
            for line in f:
                line = line.strip().split()
                para = line[0]
                value = float(line[2])
                if para in scioal_insurance_type:
                    scioal_insurance_rate += float(value)
                if para == 'JiShuH':
                    self.JiShuH = value
                if para == 'JiShuL':
                    self.JiShuL = value
        return scioal_insurance_rate



class Calculator(object):
    def __init__(self,config,number,salay):
        self.number = number
        self._calculator(config,salay)

    def _calculator(self,config,salay):
        tax_table = namedtuple('tax_table',['taxable_part','taxrate','deduction'])
        tax_list = [
          tax_table(80000,0.45,13500),
          tax_table(55000,0.35,5505),
          tax_table(35000,0.30,2755),
          tax_table(9000,0.25,1005),
          tax_table(4500,0.20,555),
          tax_table(1500,0.10,105),
          tax_table(0,0.03,0),
        ]
        start_tax_point = 3500
        self.salay = salay
        if salay <= config.JiShuL:
            scioalable_part = config.JiShuL
        elif salay >= config.JiShuH:
            scioalable_part = config.JiShuH
        else:
            scioalable_part = salay

        salay_of_scioal = scioalable_part * config.scioal_insurance_rate
        self.salay_of_scioal = salay_of_scioal

        real_income = salay - salay_of_scioal
        taxable_part = real_income - start_tax_point

        for taxinfo in tax_list:
            if taxable_part <= 0:
                self.salay_after_tax = real_income
                self.salay_of_tax = 0
                return None
            if taxable_part > taxinfo.taxable_part:
                self.salay_of_tax = taxable_part * taxinfo.taxrate - taxinfo.deduction
                self.salay_after_tax = salay - self.salay_of_tax - self.salay_of_scioal
                return None



class Export(object):
    def __init__(self,calculator,outfile):
       self._writefile(calculator,outfile)

    def _writefile(self,c,outfile):
        with open(outfile,'a') as f:
            spamwriter = csv.writer(f,delimiter=',')
            row = [c.number,c.salay,"%.2f" % c.salay_of_scioal,"%.2f" % c.salay_of_tax,"%.2f" % c.salay_after_tax]
            spamwriter.writerow(row)

if __name__ == '__main__':
    if len(sys.argv) != 7:
        print('Parameter Error')
        sys.exit(1)
    for arg in sys.argv[1:]:
        if arg == '-c':
            index = sys.argv.index(arg)
            conf = sys.argv[index + 1]
        if arg == '-d':
            index = sys.argv.index(arg)
            datafile = sys.argv[index + 1]
        if arg == '-o':
            index = sys.argv.index(arg)
            outfile = sys.argv[index + 1]
    config = Config(conf)
    with open(outfile,'w') as f:
        f.truncate()
    with open(datafile,'r') as f:
        spamreader = csv.reader(f)
        for row in spamreader:
            number = int(row[0])
            salay = int(row[1])
            c = Calculator(config,number,salay)
            Export(c,outfile)





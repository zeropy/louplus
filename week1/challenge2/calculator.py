#!/usr/bin/env python
# coding=utf-8

import sys
import os
from collections import namedtuple

tax_table = namedtuple('tax_table',['salay_of_tax','taxrate','deduction'])

tax_list = [
  tax_table(80000,0.45,13500),
  tax_table(55000,0.35,5505),
  tax_table(35000,0.30,2755),
  tax_table(9000,0.25,1005),
  tax_table(4500,0.20,555),
  tax_table(1500,0.10,105),
  tax_table(0,0.03,0),
]

def Calculator(number,salay):

    salay_of_tax = salay - salay * 0.165 - 3500
    if salay_of_tax <= 0:
        salay_after_insurance = salay_of_tax + 3500
        print('{:d}:{:0.2f}'.format(number,salay_after_insurance))
        return None
    for t in tax_list:
        if salay_of_tax <= t.salay_of_tax:
            continue
        tax = salay_of_tax * t.taxrate - t.deduction
        salay_after_tax = salay_of_tax - tax + 3500
        print('{:d}:{:.2f}'.format(number,salay_after_tax))
        return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Parameter Error')
        sys.exit(1)
    try:
        for i in  sys.argv[1:]:
            t = i.strip().split(':')
            num = int(t[0])
            salay = int(t[1])
            Calculator(num,salay)
    except TypeError as e:
        print('Parameter Error')


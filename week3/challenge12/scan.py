#!/usr/bin/env python
# coding=utf-8

import sys
import socket
from ipaddress import IPv4Address,AddressValueError
from argparse import ArgumentParser

class Args(object):
    def __init__(self,args):
        self.option = self._parse_args(args)

    def _parse_args(self,args):
        parse = ArgumentParser()
        parse.add_argument('--host')
        parse.add_argument('--port')
        option = parse.parse_args()
        try:
            IPv4Address(option.host)
        except AddressValueError:
            print('host must specified IPv4Address.')
            exit()
        if option.port is None:
            print('Must specified port')
            exit()
        return option

class Scan(object):
    @staticmethod
    def scan_port(ip,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        address = (ip,port)
        res = sock.connect_ex(address)
        if res == 0:
            print('{} opend'.format(port))
            return None
        else:
            print('{} closed'.format(port))
            return None

    @classmethod
    def scan_range(cls,ip,start_port,end_port):
        if start_port > end_port:
            print('start port must more than the end port.')
            exit()
        end_port += 1
        for port in range(start_port,end_port):
            cls.scan_port(ip,port)

    def  scan(self,ip,ports):
        '''
           ports: port or port_range,like 80 or 80-83
        '''
        try:
            start_port,end_port = ports.split('-')
            start_port = int(start_port)
            end_port = int(end_port)
        except ValueError as e:
            start_port = int(ports)
            end_port = start_port
        self.scan_range(ip,start_port,end_port)


class Execute(object):
    def __init__(self,args):
        arg = Args(args)
        self.ip = arg.option.host
        self.ports = arg.option.port
        self.scan = Scan()

    def executer(self):
        self.scan.scan(self.ip,self.ports)

if __name__ == '__main__':
    execute = Execute(sys.argv[1:])
    execute.executer()



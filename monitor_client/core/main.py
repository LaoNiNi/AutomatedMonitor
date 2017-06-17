#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/15 23:48"

from .client import ClientHandlers

class main_command(object):
    #初始化
    def __init__(self,sys_argv):
        self.sys_argv = sys_argv
        if len(sys_argv) < 2 :
            exit("请输入start或stop")
        else:
            self.entry_command()

    #根据命令调用方法
    def entry_command(self):
        print("##############################################")
        if hasattr(self,self.sys_argv[1]):
            func = getattr(self,self.sys_argv[1])
            return func()
        else:
            print("请输入正确的命令")


    def start(self):
        client = ClientHandlers()
        client.forever_run()

    def stop(self):
        pass





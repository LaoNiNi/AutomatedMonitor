#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/4/30 17:02"


#_*_coding:utf-8_*_
__author__ = 'Alex Li'

from .linux import sysinfo,load,cpu_mac,cpu,memory,network,host_alive


def LinuxSysInfo():
    #print __file__
    return  sysinfo.collect()


def WindowsSysInfo():
    from windows import sysinfo as win_sysinfo
    return win_sysinfo.collect()

def get_linux_cpu():
    return cpu.monitor()

def host_alive_check():
    return host_alive.monitor()

def GetMacCPU():
    #return cpu.monitor()
    return cpu_mac.monitor()

def GetNetworkStatus():
    return network.monitor()

def get_memory_info():
    return memory.monitor()


def get_linux_load():
    return load.monitor()
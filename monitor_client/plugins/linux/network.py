#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/2 23:27"

import psutil
def monitor(frist_invoke=1):
    """
    {'em1': snetio(bytes_sent=10094978, bytes_recv=35218957, packets_sent=63881, packets_recv=67980, errin=0, errout=0, dropin=0, dropout=0),
    'lo': snetio(bytes_sent=2805824, bytes_recv=2805824, packets_sent=34624, packets_recv=34624, errin=0, errout=0, dropin=0, dropout=0)}
    :param frist_invoke:
    :return:
    """
    ret = psutil.net_io_counters(pernic=True)

    #print(result)
    value_dic = {'status':0, 'data':{}}
    for nic_name,values in ret.items():

        value_dic['data'][nic_name] = {"bytes_sent":values.bytes_sent, "bytes_recv":values.bytes_recv,"packets_sent":values.packets_sent,"packets_recv":values.packets_recv}


    return value_dic


if __name__ == '__main__':
    print(type(monitor()),monitor())


#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = "BIGNI"
__date__ = "2017/5/7 6:23"

import json,time,copy

from automated_monitor import settings
#数据实例
class DataStore(object):
    #初始化client传过来的数据
    def __init__(self,client_id,service_name,data,redis_obj):
        self.client_id = client_id
        self.service_name = service_name
        self.data = data
        self.redis_conn_obj = redis_obj
        #处理进程并保存数据
        self.process_and_save()

    def get_data_slice(self,lastest_data_key,optimization_interval):
        """

        :param lastest_data_key:
        :param optimization_interval: 拿到这个时间戳，eg：1800s 取前1800s里的所有数据
        :return:
        """
        #获取最新数据
        all_real_data = self.redis_conn_obj.lrange(lastest_data_key,1,-1)
        data_set = []
        for item in all_real_data:
            data = json.loads(item.decode('utf8'))
            if len(data) == 2:
                service_data,last_save_time = data
                #判断是否小于时间戳
                if time.time() - last_save_time <= optimization_interval:
                    data_set.append(data)
                else:
                    pass
        return data_set

    def get_average(self,data_set):
        """
        计算平均数
        :param data_set:
        :return:
        """
        if len(data_set) >0:
            return sum(data_set) /len(data_set)
        else:
            return 0

    def get_max(self,data_set):
        """
        计算最大值
        :param data_set:
        :return:
        """
        if len(data_set) >0:
            return max(data_set)
        else:
            return 0

    def get_min(self,data_set):
        """
        计算最小值
        :param data_set:
        :return:
        """
        if len(data_set) >0:
            return min(data_set)
        else:
            return 0

    def get_mid(self,data_set):
        """
        计算中位数
        :param data_set:
        :return:
        """
        data_set.sort()
        #[1,4,99,32,8,9,4,5,9]
        #[1,3,5,7,9,22,54,77]
        if len(data_set) >0:
            return data_set[  int(len(data_set)/2) ]
        else:
            return 0

    def get_optimized_data(self,data_set_key, raw_service_data):
        """
        计算平均数、最大数、最小数、中位数
        calculate out ava,max,min,mid value from raw service data set
        :param data_set_key:
        :param raw_service_data:这种格式：[[{data},'time'],]
        :return:
        """
        #index_init =[avg,max,min,mid]
        print("get_optimized_data:", raw_service_data[0])
        #拿到字典里的所有keys
        service_data_keys = raw_service_data[0][0].keys()  # [iowait, idle,system...]
        #取出第一个字典
        first_service_data_point = raw_service_data[0][0]
        #创建一个空dict，用于保存优化后的数据。
        optimized_dic = {} #set a empty dic, will save optimized data later
        #这里是提前约定好的，如果监控的服务下有子服务，eg网卡有多个，子服务就存在data的value
        if 'data' not in first_service_data_point:
            for key in first_service_data_point:
                optimized_dic[key] = []

            # optimized_dic = optimized_dic.fromkeys(first_service_data_point,[])
            tmp_data_dic = copy.deepcopy(optimized_dic)  # 为了临时存最近n分钟的数据 ,把它们按照每个指标 都 搞成一个一个列表 ,来存最近N分钟的数据
            print("tmp data dic:", tmp_data_dic)
            for service_data_item, last_save_time in raw_service_data:  # loop 最近n分钟的数据
                # print(service_data_item)
                for service_index, v in service_data_item.items():  # loop 每个数据点的指标
                    # print(service_index,v)
                    try:
                        tmp_data_dic[service_index].append(round(float(v), 3))  # 把这个点的当前这个指标 的值 添加到临时dict中
                    except ValueError as e:
                        pass
            #遍历取出服务的各个指标，进行数据优化
            for service_k,v_list in tmp_data_dic.items():
                print(service_k,v_list)
                #平均数
                avg_res = self.get_average(v_list)
                #最大值
                max_res = self.get_max(v_list)
                #最小值
                min_res = self.get_min(v_list)
                #中位数
                mid_res = self.get_mid(v_list)
                #把优化的数据存字典里
                optimized_dic[service_k]= [avg_res,max_res,min_res,mid_res]
                print(service_k, optimized_dic[service_k])

        else:
            #如果有嵌套服务，比如多网卡，多硬盘等
            """
            {'status': 0, 'data': {b'lo': {'t_out': b'0.00', 't_in': b'0.00'}, b'eth0': {'t_out': b'0.00', 't_in': b'0.00'}}}
            """
            for service_item_key,v_dic in first_service_data_point['data'].items():
                optimized_dic[service_item_key] = {}
                for k2,v2 in v_dic.items():
                    optimized_dic[service_item_key][k2] = []#{etho0:{t_in:[],t_out:[]}}

            tmp_data_dic = copy.deepcopy(optimized_dic)
            if tmp_data_dic:
                print("临时待优化数据：",tmp_data_dic)
                for service_data_item, last_save_time in raw_service_data:  # loop最近n分钟数据
                    for service_index, val_dic in service_data_item['data'].items():
                        # print(service_index,val_dic)
                        # service_index这个值 相当于eth0,eth1...
                        for service_item_sub_key, val in val_dic.items():
                            # 上面这个service_item_sub_key相当于t_in,t_out
                            # if service_index == 'lo':
                            # print(service_index,service_item_sub_key,val)
                            tmp_data_dic[service_index][service_item_sub_key].append(round(float(val), 2))
                                # 上面的service_index变量相当于 eth0...
                for service_k, v_dic in tmp_data_dic.items():
                    for service_sub_k, v_list in v_dic.items():
                        print(service_k, service_sub_k, v_list)
                        avg_res = self.get_average(v_list)
                        max_res = self.get_max(v_list)
                        min_res = self.get_min(v_list)
                        mid_res = self.get_mid(v_list)
                        optimized_dic[service_k][service_sub_k] = [avg_res, max_res, min_res, mid_res]
                        print(service_k, service_sub_k, optimized_dic[service_k][service_sub_k])
            else:
                print("\033[41;1mMust be sth wrong with client report data\033[0m")
        print("optimized empty dic:", optimized_dic)

        return optimized_dic

    def save_optimized_data(self,data_series_key_in_redis,optimized_data):
        """
        把优化的数据保存到数据库
        :param data_series_key_in_redis:
        :param optimized_data:
        :return:
        """
        self.redis_conn_obj.rpush(data_series_key_in_redis, json.dumps([optimized_data, time.time()]))

    #进程和数据保存嵌套
    def process_and_save(self):

        print("\033[42;1m---service data-----------------------\033[0m")
        if self.data['status'] == 0:
            """
            STATUS_DATA_OPTIMIZATION = {
            'lastest':[0,600],
            '10mins':[600,600],#4天
            '30mins':[1800,600],#14天
            '60mins':[3600,600],#25天
            }
            """
            for key,data_series_val in settings.STATUS_DATA_OPTIMIZATION.items():
                #通过key取出最后一个点的值
                data_series_key_in_redis = "StatusData_{client_id}_{service_name}_{key}".format(client_id=self.client_id,
                                                                                                service_name=self.service_name,key=key)
                #通过这个key去redis里查找,取出上一个时间戳
                last_point_from_redis = self.redis_conn_obj.lrange(data_series_key_in_redis,-1,-1)
                #如果时间点不存在可能时间还没到,那么传入一个空值，时间戳进去
                if not last_point_from_redis:
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([None,time.time()] ))

                #当等于0时，表示当前值，不需要进行优化
                if data_series_val[0] == 0:
                    self.redis_conn_obj.rpush(data_series_key_in_redis,json.dumps([self.data,time.time()]))

                #如果不为零，则表示需要优化(或者将要优化)
                else:
                    last_point_data, last_point_save_time = \
                        json.loads(self.redis_conn_obj.lrange(data_series_key_in_redis,-1,-1)[0].decode("utf8"))
                    if time.time() - last_point_save_time >= data_series_val[0]:
                        lastest_data_key_in_redis = "StatusData_{client_id}_{service_name}_lastest".format(client_id=self.client_id,
                                                                                                           service_name=self.service_name)
                        print("calulating data for key:\033[31;1m{ret}\033[0m".format(ret=data_series_key_in_redis))
                        #拿到在这个时间间隔内的所有数据返回list，
                        data_set = self.get_data_slice(lastest_data_key_in_redis,data_series_val[0])
                        print("----->",data_set)
                        if len(data_set) > 0:
                            #通过下面的方法，把拿到的数据进行优化，并返回结果。
                            optimized_data = self.get_optimized_data(data_series_key_in_redis,data_set)
                            if optimized_data:
                                self.save_optimized_data(data_series_key_in_redis,optimized_data)

                #存储在redis里的数据不能超过settings里的指定值
                if self.redis_conn_obj.llen(data_series_key_in_redis) >= data_series_val[1]:
                    self.redis_conn_obj.lpop(data_series_key_in_redis)
        else:
            print("report data is invalid::",self.data)
            raise ValueError




















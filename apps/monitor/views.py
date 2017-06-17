from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

from monitor.backends import redis_conn

from .serializer import ClientHandler
from .backends import data_optimization
from automated_monitor import settings

#根据redis配置反问redis connection_pool
REDIS_OBJ = redis_conn.redis_conn(settings)

class client_config_view(View):

    #返回客户端需要监控信息
    def get(self,request,client_id):
        #获取client信息
        # client_configs = ClientHandler(client_id).fetch_configs()
        client_obj = ClientHandler(client_id)
        client_config = client_obj.fetch_configs()
        print("客户端ID",client_id)
        if client_config:
            return HttpResponse(json.dumps(client_config),content_type="application/json")



# class service_data_report_view(View):
#     #client统一汇报
#     @csrf_exempt
#     def post(self,request):
#         print("----->",request.POST)
#         print("主机ID={host_id},服务名称={service}".format(host_id=request.POST.get("client_id"),
#                                                      service=request.POST.get("service_name")))
#         data = json.loads(request.POST['data'])
#
#         client_id = request.POST.get("client_id")
#         service_name = request.POST.get("service_name")
#
#         print(data)
@csrf_exempt
def service_data_report_view(request):

    if request.method == "POST":
        # print("----->", request.POST)
        try:
            #获取到client传过来的值
            receive_data = json.loads(request.body.decode('utf8'))
            client_id = receive_data["client_id"]
            service_name = receive_data["service_name"]
            print("主机ID={host_id},服务名称={service}".format(host_id=client_id,
                                                                 service=service_name))
            #获取数据
            data = receive_data['data']
            print("----------->",data)

            #存储数据
            data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)



        except Exception as e:

            print('------exec', "\033[31;1m%s\033[0m" % e)


    return HttpResponse(json.dumps("---report success---"))
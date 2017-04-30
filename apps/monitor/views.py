from django.shortcuts import render

# Create your views here.

from django.views.generic import View
from django.http import HttpResponse
import json

from .serializer import ClientHandler


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


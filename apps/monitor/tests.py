from django.test import TestCase

# Create your tests here.


# # 标准格式：
# [[{data1},time1],[{data2},time2],...]
#
# # 例如：
# [[{"status":0,"iowait":1.7,"system":17.44},14636534.86],[{data2},time2],...]
#
# # 有嵌套服务的情况：
# [[{"status":0,"data":{'io':{"t_in":0.10,"t_out":0.01},
#                       'docker0':{"t_in":0.10,"t_out":0.01}
#                       }
#    },'14636534.86'
#   ]
#  ]

#一个服务的keys:StatusData_client_id_ServerName_time
StatusData_2_LinuxCPU_30mins
StatusData_2_LinuxCPU_60mins
StatusData_2_LinuxCPU_10mins
StatusData_2_LinuxCPU_lastest

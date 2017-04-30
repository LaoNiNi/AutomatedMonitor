#!_*_coding:utf8_*_

from django.db import models
from monitor import auth
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

# Create your models here.



#主机表
class Host(models.Model):
    #主机名唯一
    name =  models.CharField(max_length=64,unique=True,verbose_name="主机名")
    #IP地址唯一
    ip_addr =  models.GenericIPAddressField(unique=True,verbose_name="IP地址")
    #主机组
    host_groups = models.ManyToManyField('HostGroup',blank=True,verbose_name="主机组") # A B C
    #默认模板
    templates = models.ManyToManyField("Template",blank=True,verbose_name="默认模板") # A D E
    monitored_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )
    #监控选择
    monitored_by = models.CharField(max_length=64,choices=monitored_by_choices,verbose_name="监控方式")
    status_choices= (
        (1,'Online'),
        (2,'Down'),
        (3,'Unreachable'),
        (4,'Offline'),
        (5,'Problem'),
    )
    #
    host_alive_check_interval = models.IntegerField( default=30,verbose_name="主机存活状态检测间隔")
    #主机状态
    status = models.IntegerField(choices=status_choices,default=1,verbose_name="主机状态")
    #备注信息
    memo = models.TextField(blank=True,null=True,verbose_name="备注信息")

    class Meta:
        verbose_name = '主机信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#主机组表
class HostGroup(models.Model):
    #主机组名
    name =  models.CharField(max_length=64,unique=True,verbose_name="主机组名")
    #主机组模板
    templates = models.ManyToManyField("Template",blank=True,verbose_name="主机组模板")
    #备注信息
    memo = models.TextField(blank=True,null=True,verbose_name="备注信息")

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#一个服务下有多个指标，指标表
class ServiceIndex(models.Model):
    #指标名称
    name = models.CharField(max_length=64,verbose_name="指标名称")
    #具体指标，比如cpu下的idle
    key =models.CharField(max_length=64)
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string")
    )
    #指标数据类型
    data_type = models.CharField(max_length=32,choices=data_type_choices,default='int',verbose_name="指标数据类型")
    #备注
    memo = models.CharField(max_length=128,blank=True,null=True,verbose_name="备注")

    class Meta:
        verbose_name = '指标表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s.%s" %(self.name,self.key)


#服务表
class Service(models.Model):
    #服务名称
    name = models.CharField(max_length=64,unique=True,verbose_name="服务名称")
    #监控间隔
    interval = models.IntegerField(default=60,verbose_name="监控间隔")
    #插件名,client拿到它来进行监控
    plugin_name = models.CharField(max_length=64,default='n/a',verbose_name="插件名")
    #指标列表,比如CPu下有多个指标，是一对多的关系
    items = models.ManyToManyField('ServiceIndex',blank=True,verbose_name="指标列表")
    #子服务
    has_sub_service = models.BooleanField(default=False,help_text=u"如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡",verbose_name="子服务") #如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    #备注
    memo = models.CharField(max_length=128,blank=True,null=True,verbose_name="备注")

    class Meta:
        verbose_name = '服务名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    #def get_service_items(obj):
    #    return ",".join([i.name for i in obj.items.all()])


#模板表
class Template(models.Model):
    name = models.CharField(u'模版名称',max_length=64,unique=True)
    services = models.ManyToManyField('Service',verbose_name=u"服务列表")
    triggers = models.ManyToManyField('Trigger',verbose_name=u"触发器列表",blank=True)

    class Meta:
        verbose_name = '模板'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



#触发一个报警，由多个指标来判断，触发关联表,一个表达式只能关联一个trigger
class TriggerExpression(models.Model):
    #所属触发器
    trigger = models.ForeignKey('Trigger',verbose_name="所属触发器")
    #关联服务
    service = models.ForeignKey(Service,verbose_name="关联服务")
    #关联服务指标
    service_index = models.ForeignKey(ServiceIndex,verbose_name="关联服务指标")
    #只监控专门指定的指标key
    specified_index_key = models.CharField(verbose_name="只监控专门指定的指标key",max_length=64,blank=True,null=True)
    operator_type_choices = (('eq','='),('lt','<'),('gt','>'))
    #运算符
    operator_type = models.CharField(u"运算符",choices=operator_type_choices,max_length=32)
    data_calc_type_choices = (
        ('avg','Average'),
        ('max','Max'),
        ('hit','Hit'),
        ('last','Last'),
    )
    #数据处理方式
    data_calc_func= models.CharField(choices=data_calc_type_choices,max_length=64,verbose_name="数据处理方式")
    #函数传入参数
    data_calc_args = models.CharField(help_text="若是多个参数,则用,号分开,第一个值是时间",max_length=64,verbose_name="函数传入参数")
    #阈值
    threshold = models.IntegerField(u"阈值")


    logic_type_choices = (('or','OR'),('and','AND'))
    #与另一个表达式的关系
    logic_type = models.CharField(choices=logic_type_choices,max_length=32,blank=True,null=True,verbose_name="与一个条件的逻辑关系")
    def __str__(self):
        return "%s %s(%s(%s))" %(self.service_index,self.operator_type,self.data_calc_func,self.data_calc_args)

    class Meta:
        verbose_name = '触发器表达式'
        verbose_name_plural = verbose_name #unique_together = ('trigger_id','service')



#触发报警的，触发器表
class Trigger(models.Model):
    #触发器名称
    name = models.CharField(max_length=64,verbose_name="触发器名称")
    severity_choices = (
        (1,'Information'),
        (2,'Warning'),
        (3,'Average'),
        (4,'High'),
        (5,'Diaster'),
    )
    #expressions = models.ManyToManyField(TriggerExpression,verbose_name=u"条件表达式")
    #告警级别
    severity = models.IntegerField(choices=severity_choices,verbose_name="告警级别")

    enabled = models.BooleanField(default=True)
    #备注
    memo = models.TextField(blank=True,null=True,verbose_name="备注")

    class Meta:
        verbose_name = '触发器'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<serice:%s, severity:%s>" %(self.name,self.get_severity_display())



#触发报警后的动作类型
class Action(models.Model):
    #action名称
    name =  models.CharField(max_length=64,unique=True,verbose_name="动作名称")
    #关联哪个主机组
    host_groups = models.ManyToManyField('HostGroup',blank=True,verbose_name="主机组")
    #关联哪个主机
    hosts = models.ManyToManyField('Host',blank=True,verbose_name="主机")
    #告警条件
    conditions = models.TextField(verbose_name="告警条件")
    #触发器
    triggers = models.ManyToManyField('Trigger',blank=True,help_text=u"想让哪些trigger触发当前报警动作",verbose_name="触发器")
    #告警间隔
    interval = models.IntegerField(default=300,verbose_name="告警间隔(s)")
    #关联别的动作
    operations = models.ManyToManyField('ActionOperation',verbose_name='ActionOperation')
    #故障恢复是否要通知
    recover_notice = models.BooleanField(verbose_name='故障恢复后发送通知消息',default=True)
    #恢复后通知的主题是什么
    recover_subject = models.CharField(max_length=128,blank=True,null=True,verbose_name="通知主题")
    #通知文本
    recover_message = models.TextField(blank=True,null=True,verbose_name="通知文本")
    #是否停用
    enabled = models.BooleanField(default=True,verbose_name="是否停用")

    class Meta:
        verbose_name = '触发报警后的动作类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#触发报警后的具体动作
class ActionOperation(models.Model):
    name =  models.CharField(max_length=64,verbose_name="告警升级")
    step = models.SmallIntegerField(verbose_name="第n次告警",default=1,help_text="当trigger触发次数小于这个值时就执行这条记录里报警方式")
    action_type_choices = (
        ('email','Email'),
        ('sms','SMS'),
        ('script','RunScript'),
    )
    #通过告警次数，给告警级别升级，并且指定动作类型
    action_type = models.CharField(verbose_name="动作类型",choices=action_type_choices,default='email',max_length=64)
    #告警通知对象
    notifiers= models.ManyToManyField('UserProfile',verbose_name="通知对象",blank=True)
    _msg_format = '''Host({hostname},{ip}) service({service_name}) has issue,msg:{msg}'''
    #消息格式
    msg_format = models.TextField(verbose_name="消息格式",default=_msg_format)

    class Meta:
        verbose_name = '触发报警后的具体动作'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name



#主机维护表
class Maintenance(models.Model):

    name =  models.CharField(max_length=64,unique=True)
    #主机
    hosts = models.ManyToManyField('Host',verbose_name='主机',blank=True)
    #主机组
    host_groups = models.ManyToManyField('HostGroup',verbose_name='主机组',blank=True)
    #维护内容
    content = models.TextField(verbose_name="维护内容")
    #开始时间
    start_time = models.DateTimeField()
    #结束时间
    end_time = models.DateTimeField()

    class Meta:
        verbose_name = '主机维护表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

#日志
class EventLog(models.Model):
    """存储报警及其它事件日志"""
    event_type_choices = ((0,'报警事件'),(1,'维护事件'))
    event_type = models.SmallIntegerField(choices=event_type_choices,default=0)
    host = models.ForeignKey("Host",verbose_name="Host")
    trigger = models.ForeignKey("Trigger",verbose_name="Trigger",blank=True,null=True)
    log = models.TextField(blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = '存储报警及其它事件日志'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "host%s  %s" %(self.host , self.log)



class UserProfile(auth.AbstractBaseUser, auth.PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,

    )
    password = models.CharField(_('password'), max_length=128,
                                help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))

    phone = models.BigIntegerField(blank=True,null=True)
    weixin = models.CharField(max_length=64,blank=True,null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        verbose_name='staff status',
        default=True,
        help_text='Designates whether the user can log into this admin site.',
    )
    name = models.CharField(max_length=32)
    #role = models.ForeignKey("Role",verbose_name="权限角色")

    memo = models.TextField(verbose_name='备注', blank=True, null=True, default=None)
    date_joined = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['name','token','department','tel','mobile','memo']
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):  # __str__ on Python 2
        return self.email

    # def has_perm(self, perm, obj=None):
    #     "Does the user have a specific permission?"
    #     # Simplest possible answer: Yes, always
    #     return True
    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


    @property
    def is_superuser(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    objects = auth.UserManager()

    class Meta:
        verbose_name = '账户'
        verbose_name_plural = verbose_name





''''
CPU
    idle 80
    usage  90
    system  30
    user
    iowait  50

memory :
    usage
    free
    swap
    cache
    buffer

load:
    load1
    load 5
    load 15
'''
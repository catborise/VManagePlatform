#!/usr/bin/env python  
# _#_ coding:utf-8 _*_  
from django.db import models


class VmServer(models.Model):
    server_ip = models.GenericIPAddressField(unique=True,verbose_name='Management IP')
    username = models.CharField(max_length=100,verbose_name='Username')
    passwd = models.CharField(max_length=100,blank=True,null=True,verbose_name='Password')
    hostname = models.CharField(max_length=100,blank=True,null=True,verbose_name='Hostname')
    instance = models.SmallIntegerField(blank=True,null=True,verbose_name='Instance') 
    vm_type =  models.IntegerField(verbose_name='Virtualization Type')
    mem = models.CharField(max_length=100,blank=True,null=True,verbose_name='Memory Size')
    cpu_total = models.SmallIntegerField(blank=True,null=True,verbose_name='CPU Count') 
    status =  models.SmallIntegerField(blank=True,null=True,verbose_name='Status')
    createTime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modifyTime = models.DateTimeField(auto_now=True,blank=True,null=True)
    class Meta:
        permissions = (
            ("read_vmserver", "Can read Virtual host information"),
        )
        verbose_name = 'Virtual host information'  
        verbose_name_plural = 'Virtual host information'


class VmDHCP(models.Model):
    mode = models.CharField(unique=True,max_length=100,verbose_name='dhcp type')
    drive = models.CharField(max_length=10,verbose_name='Drive type')
    brName = models.CharField(max_length=100,verbose_name='Bridge Name')
    server_ip = models.GenericIPAddressField(verbose_name='DHCP Address')
    ip_range = models.CharField(max_length=100,verbose_name='Address Pool')
    gateway = models.GenericIPAddressField(blank=True,null=True,verbose_name='Gateway Address')
    dns = models.GenericIPAddressField(blank=True,null=True,verbose_name='DNS Address') 
    dhcp_port = models.CharField(max_length=100,verbose_name='dhcp port')
    isAlive = models.SmallIntegerField(default=1,null=True, blank=True,verbose_name='Activate Now') 
    status = models.SmallIntegerField(default=1,null=True, blank=True,verbose_name='Status') 
    createTime = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    modifyTime = models.DateTimeField(auto_now=True,blank=True,null=True)
    class Meta:
        permissions = (
            ("read_vmdhcp", "Can read  Virtual Host DHCP Configuration"),
        )
        verbose_name = 'Virtual Host DHCP Configuration'  
        verbose_name_plural = ' Virtual Host DHCP Configuration'
        unique_together = (("mode", "brName"))

class VmInstance_Template(models.Model):
    name =  models.CharField(unique=True,max_length=100,verbose_name='Template Name')
    cpu =  models.SmallIntegerField(verbose_name='Cpu Count')
    mem =  models.SmallIntegerField(verbose_name='Memory Size')
    disk =  models.SmallIntegerField(verbose_name='Disk Size') 
    class Meta:
        permissions = (
            ("read_vminstance_template", "Can read Virtual host template"),
        )
        verbose_name = 'Virtual host template'  
        verbose_name_plural = 'Virtual host template'
        
        
class VmServerInstance(models.Model):  
    server = models.ForeignKey('VmServer') 
    name =  models.CharField(max_length=100,verbose_name='Instance Name')
    cpu = models.SmallIntegerField(verbose_name='CPU Count') 
    mem = models.IntegerField(verbose_name='Memory Size')
    status = models.SmallIntegerField(verbose_name='Status')
    owner =  models.CharField(max_length=50,blank=True,null=True,verbose_name='Owner')
    rate_limit = models.SmallIntegerField(blank=True,null=True,verbose_name='Network card speed limit')
    token = models.CharField(max_length=100,blank=True,null=True,verbose_name='Token')
    ips = models.TextField(max_length=200,blank=True,null=True,verbose_name='IP address')
    vnc = models.SmallIntegerField(blank=True,null=True,verbose_name='VNC port')
    class Meta:
        permissions = (
            ("read_vmserver_instance", "Can read Virtual host instance"),
        )
        verbose_name = 'Virtual host instance'  
        verbose_name_plural = 'Virtual host instance'  
    unique_together = (("server", "name"))    
        

        
class VmLogs(models.Model): 
    server_id = models.IntegerField(verbose_name='Host id',blank=True,null=True,default=None)
    vm_name = models.CharField(max_length=50,verbose_name='Virtual machine name',default=None)
    content = models.CharField(max_length=100,verbose_name='Operation content',default=None)
    user =  models.CharField(blank=True,null=True,max_length=20,verbose_name='User')
    status = models.SmallIntegerField(verbose_name='Result of',blank=True,null=True) 
    isRead = models.SmallIntegerField(verbose_name='Has Read',blank=True,null=True) 
    result = models.TextField(verbose_name='Reason for failure',blank=True,null=True) 
    create_time = models.DateTimeField(auto_now_add=True,blank=True,null=True,verbose_name='Execution time')
    class Meta:
        permissions = (
            ("read_vmlogs", "Can read Virtual host operation log"),
        )
        verbose_name = 'Virtual host operation log'  
        verbose_name_plural = 'Virtual host operation log' 

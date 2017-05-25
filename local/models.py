# encoding: utf-8
from django.db import models


class Host(models.Model):
    vm_name = models.CharField("主机名", max_length=120, )
    vm_ip = models.CharField("IP地址", max_length=120)
    apps_list = models.CharField("APP列表", max_length=500)

    def __str__(self):
        return self.vm_name


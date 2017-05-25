# encoding: utf-8
from django.db import models
from django.utils import timezone
from django.utils.html import format_html


class Host(models.Model):
    hostname = models.CharField('主机名称', max_length=120)
    ipadd_internet = models.CharField('公网IP', max_length=120)
    ipadd_internal = models.CharField('内网IP', max_length=120)
    status = models.CharField('状态', max_length=20, default='Running')
    zone = models.CharField('可用区', max_length=120)
    os_name = models.CharField('系统类型', max_length=120)
    config = models.CharField('硬件配置', max_length=300)
    time_created = models.DateTimeField('创建时间')
    time_release = models.DateTimeField('截止时间')
    image_name = models.CharField(max_length=200)
    instance_id = models.CharField(max_length=120, primary_key=True)
    ssh_port = models.IntegerField('ssh端口', default=22)

    def __unicode__(self):
        return self.hostname

    def has_days(self):
        days = (self.time_release - timezone.now()).days
        if days > 20000:
            return format_html('<span style="color: #FF00FF">000</span>')

        if days < 10:
            return format_html('<span style="color: #FF0000">{}</span>', days)

        return days
    has_days.short_description = u'剩余天数'

    class Meta:
        ordering = ('hostname',)
        verbose_name_plural = u'主机信息'


class Application(models.Model):
    app_name = models.CharField('应用名称', max_length=120)
    hosts = models.ManyToManyField(Host)

    def __unicode__(self):
        return self.app_name

    def get_hosts(self):
        hs = []
        for h in self.hosts.all():
            hs.append(h.hostname)
        return hs
    get_hosts.short_description = u'所在主机'

    class Meta:
        ordering = ('app_name',)
        verbose_name_plural = u'应用信息'


# encoding=utf-8
import json
from django.core.management.base import BaseCommand
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest, DescribeRegionsRequest
from django.conf import settings
from aliyun.models import Host


def get_regions(c):
    request = DescribeRegionsRequest.DescribeRegionsRequest()
    request.set_accept_format('json')
    request.get_location_service_code()
    result = c.do_action_with_exception(request)
    return result


def get_hosts(c):
    request = DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_PageSize(100)
    result = c.do_action_with_exception(request)
    return json.loads(result)


def sync_to_db(host):
    h = Host()
    h.os_name = host["OSName"]
    h.ipadd_internal = host["InnerIpAddress"]["IpAddress"][0]
    h.ipadd_internet = host["PublicIpAddress"]["IpAddress"][0]
    h.config = str(host["Cpu"]) + u'核, ' + str(host["Memory"]) + "G, " + host["InstanceTypeFamily"]
    h.hostname = (host["InstanceName"]).lower()
    h.time_created = host["CreationTime"]
    h.time_release = host["ExpiredTime"]
    h.zone = host["ZoneId"]
    h.status = host["Status"]
    h.instance_id = host["InstanceId"]
    h.image_name = host["ImageId"]
    h.save()


def parse_hosts(hosts):
    for h in hosts["Instances"]["Instance"]:
        sync_to_db(h)


class Command(BaseCommand):
    help = "同步阿里云资源信息到本地"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        clt = client.AcsClient(settings.KEY, settings.SECRET, settings.ZONE)
        hosts = get_hosts(clt)
        parse_hosts(hosts)

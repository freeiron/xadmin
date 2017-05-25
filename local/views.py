from django.shortcuts import render
from .models import Host


def index(request):
    hosts = Host.objects.all()
    context = {'hosts': hosts}
    return render(request, 'hosts/index.html', context)

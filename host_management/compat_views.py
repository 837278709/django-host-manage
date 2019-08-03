'''
Created on Dec 18, 2018
'''
from .models import Host

def get_host_list() -> list:
    rv = Host.objects.all().values()
    rv = list(rv)
    return rv

def get_host(uuid: str):
    rv = Host.objects.get(pk=uuid)
    return rv

def del_host(uuid: str):
    host = Host.objects.get(pk=uuid)
    host.delete()

def add_host(name: str, address: int):
    host = Host(name=name, address=address)
    host.save()
    return host.id

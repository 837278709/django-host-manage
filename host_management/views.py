# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from collections import OrderedDict
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Host, BusinessLine
from .serializers import HostSerializer
from . import ansible_cli



def run_shell(request):
    hosts = ['localhost,127.0.0.1']
    cmd = "cat /etc/hostname"
    ansible_cli.shell_cli(hosts, shell_cmd=cmd,
                          module="shell", remote_user="root")
    return


def get_host_info(request):
    hosts = ['localhost,192.168.31.247']
    cmd = "gather_subset=min"
    ansible_cli.shell_cli(hosts, shell_cmd=cmd,
                          module="setup", remote_user="root")
    return


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('business_line', BusinessLine.objects.values('id','name',)),
            ('page', None),
            ('count_page', None),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('table_header', None),
            ('results', data)
        ]))


class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,
                       DjangoFilterBackend)
    ordering_fields = ('create_time', 'update_time')
    ordering = ('-update_time',)
    search_fields = ('hostname', )
    filter_fields = ('business_line', 'address', 'os_type', 'name', 'domain')

    def list(self, request, *args, **kwargs):
        table_header = [{
            "title": "IP",
            "index": "name"
        }, {
            "title": "主机名",
            "index": "hostname"
        }, {
            "title": "内存",
            "index": "memory"
        }, {
            "title": "磁盘",
            "index": "disk"
        }, {
            "title": "网络域",
            "index": "domain"
        }, {
            "title": "CPU 数",
            "index": "cpu"
        }, {
            "title": "地址",
            "index": "address_name"
        }, {
            "title": "业务线",
            "index": "business_line"
        }, {
            "title": "创建时间",
            "index": "create_time"
        }, {
            "title": "更新时间",
            "index": "update_time"
        }, {
            "title": "备注信息",
            "index": "note"
        }]
        rv = super(HostViewSet, self).list(request, *args, **kwargs)
        if not rv.data.get("table_header"):
            rv.data["table_header"] = table_header
        page_size = request.query_params.get('page_size')
        count = rv.data.get("count")
        if not page_size:
            page_size = StandardResultsSetPagination.page_size
        else:
            page_size = int(page_size)
        if not rv.data.get("count_page"):
            rv.data["count_page"] = count // page_size + 1
        rv.data["page"] = request.query_params.get('page')
        return rv

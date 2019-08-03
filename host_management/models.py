# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from uuid import uuid1
from inflection import underscore


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid1, editable=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BusinessLine(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = underscore("BusinessLine")
    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class Host(Base):
    name = models.GenericIPAddressField(db_column="ip")
    host_user = models.CharField(max_length=50, null=True)
    host_pass = models.CharField(max_length=100, null=True)
    memory = models.PositiveSmallIntegerField(null=True)
    disk = models.PositiveSmallIntegerField(null=True)
    hostname = models.CharField(max_length=50, null=True)
    domain = models.CharField(max_length=100, null=True)
    cpu = models.PositiveSmallIntegerField(null=True)
    note = models.TextField(null=True)
    business_line = models.ManyToManyField(BusinessLine,
                                           blank=True)
    LINUX = 2
    OS_TYPE_CHOICES = (
        (0, 'HP-UX'),
        (1, 'AIX'),
        (LINUX, 'LINUX'),
    )
    os_type = models.PositiveSmallIntegerField(
        choices=OS_TYPE_CHOICES,
        null=True
    )
    ADDRESS_CHOICES = (
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
    )
    address = models.PositiveSmallIntegerField(
        choices=ADDRESS_CHOICES,
    )

    class Meta:
        unique_together = (("name", "address"),)

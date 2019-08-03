'''
Created on Oct 19, 2018
@author: Jack
'''
from .models import Host, BusinessLine
from rest_framework import serializers
from django.conf import settings


class BaseSerializer(serializers.ModelSerializer):
    create_user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    update_user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    # datetime format 2018-11-05 12:00
    create_time = serializers.DateTimeField(read_only=True,
                                            format=settings.DATETIME_FORMAT)
    update_time = serializers.DateTimeField(read_only=True,
                                            format=settings.DATETIME_FORMAT)


class HostSerializer(BaseSerializer):
    name = serializers.IPAddressField()
    address_name = serializers.SerializerMethodField()
    business_line = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=BusinessLine.objects.all(),
        required=False
    )
    business_line_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=BusinessLine.objects.all(),
        required=False,
        write_only=True)

    class Meta:
        model = Host
        fields = '__all__'

    def get_address_name(self, obj):
        return obj.get_address_display()
    def update(self, instance, validated_data):
        instance = super(HostSerializer, self).update(instance, validated_data)
        field = getattr(instance, "business_line")
        value = validated_data.get("business_line_id")
        if value is not None:
            field.set(value)
            instance.save()
        return instance
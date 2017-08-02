from django.contrib import admin

# Register your models here.

from .models import *


@admin.register(APP)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'desc')
    search_fields = ('name', 'desc')


@admin.register(APIInfo)
class APIInfoAdmin(admin.ModelAdmin):
    list_display = ('desc', 'method', 'endpoint', 'app_name', 'version', 'resource_name', 'is_auth_required')
    search_fields = ('app__name', 'desc', 'endpoint')
    list_filter = ('app', )


@admin.register(APIParameter)
class APIParameterAdmin(admin.ModelAdmin):
    list_display = ('desc', 'name', 'parameter_type', 'note')
    search_fields = ('name', 'desc')


@admin.register(APIRequestParameter)
class APIRequestParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'parameter', 'is_required', 'note')
    search_fields = ('api__desc', 'api__endpoint', 'parameter__name')
    list_filter = ('api',)


@admin.register(APIResponseParameter)
class APIResultParameterAdmin(admin.ModelAdmin):
    list_display = ('name', 'parameter', 'is_required', 'note')
    search_fields = ('api__desc', 'api__endpoint', 'parameter__name')
    list_filter = ('api',)

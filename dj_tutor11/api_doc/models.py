# coding: utf-8

# __all__ = ('APP', 'APIInfo', 'APIParameter', 'APIResult')
import json
from django.db import models
from common.models import BaseModel
from .choices import HttpMethodChoice, APIValueType
# Create your models here.


class APP(BaseModel):
    name = models.CharField(max_length=100, verbose_name=u'应用名称')
    desc = models.TextField(verbose_name=u'应用描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name_plural = verbose_name = u'应用'


class APIInfo(BaseModel):

    app = models.ForeignKey(APP, related_name='apis', verbose_name=u'所属应用')
    endpoint = models.CharField(max_length=200, verbose_name=u'请求URL')
    resource_name = models.CharField(max_length=200, verbose_name=u'资源名称', null=True, blank=True)
    desc = models.TextField(verbose_name=u'API描述')
    is_auth_required = models.BooleanField(verbose_name=u'需要验证?')
    note = models.TextField(verbose_name=u'备注', null=True, blank=True)
    method = models.IntegerField(verbose_name=u'请求方法', choices=HttpMethodChoice.choices, default=HttpMethodChoice.GET)
    version = models.CharField(max_length=20, verbose_name=u'版本', default='v1')

    def app_name(self):
        return self.app.name
    app_name.short_description = u'应用名'

    def __unicode__(self):
        return '{}: {} {}'.format(self.desc, self.get_method_display(), self.endpoint)

    def __str__(self):
        return self.__unicode__()

    @property
    def api_results(self):
        return APIResponseParameter.enables.filter(api=self).all()

    @property
    def api_parameters(self):
        return APIRequestParameter.enables.filter(api=self).all()

    def get_method(self):
        return self.get_method_display().split(' ')[-1]

    def details(self):
        info = {}
        info['app'] = self.app.name
        info['description'] = self.desc
        info['usage'] = '{}: <i>/api/{}{}</i>'.format(self.get_method_display(), self.version, self.endpoint)
        info['is_auth_required'] = self.is_auth_required
        info['version'] = self.version
        info['note'] = self.note

        # requests = {}
        # for request in self.api_parameters:
        #     param = request.parameter
        #     requests[param.name] = '{} ({})'.format(param.get_parameter_type_display(), param.desc)
        info['requests'] = self.api_parameters

        # results = {}
        # for result in self.api_results:
        #     param = result.parameter
        #     results[param.name] = '{} ({})'.format(param.get_parameter_type_display(), param.desc)
        info['results'] = self.api_results
        # return json.loads(json.dumps(info))
        return info

    class Meta:
        verbose_name_plural = verbose_name = u'API详情'


class APIParameter(BaseModel):
    name = models.CharField(max_length=100, verbose_name=u'参数名称')
    parameter_type = models.IntegerField(choices=APIValueType.choices, default=APIValueType.STRING, verbose_name=u'参数类型')
    desc = models.CharField(max_length=100, verbose_name=u'参数描述')
    note = models.TextField(verbose_name=u'备注', null=True, blank=True)

    @property
    def type_(self):
        return self.result_type

    def __unicode__(self):
        return '{} <{}>'.format(self.name, self.get_parameter_type_display())

    def __str__(self):
        return self.__unicode__()

    class Meta:
        verbose_name_plural = verbose_name = u'API参数'


class APIRequestParameter(BaseModel):
    api = models.ForeignKey(APIInfo, related_name='parameters', verbose_name=u'所属API')
    parameter = models.ForeignKey(APIParameter, related_name='reqapis', verbose_name=u'参数名称')
    is_required = models.BooleanField(verbose_name=u'是否必要?')
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'备注')

    def __unicode__(self):
        return '{} : {}'.format(self.api.desc, self.parameter)

    def __str__(self):
        return self.__unicode__()

    def name(self):
        return '{} '.format(self.api)
    name.short_description = 'Name'

    class Meta:
        verbose_name_plural = verbose_name = u'API请求参数'


class APIResponseParameter(BaseModel):
    api = models.ForeignKey(APIInfo, related_name='results', verbose_name=u'所属API')
    parameter = models.ForeignKey(APIParameter, related_name='retapis', verbose_name=u'字段名称')
    is_required = models.BooleanField(verbose_name=u'是否必要?')
    note = models.TextField(verbose_name=u'备注')

    def __unicode__(self):
        return '{} : {}'.format(self.api.desc, self.parameter)

    def __str__(self):
        return self.__unicode__()

    def name(self):
        return '{} '.format(self.api)
    name.short_description = 'Name'

    class Meta:
        verbose_name_plural = verbose_name = u'API返回数据'


class Test(models.Model):
    """
    Description: Model Description
    """

    name = models.CharField(max_length=200, verbose_name='test')

    class Meta:
        verbose_name=verbose_name_plural= u'Test'

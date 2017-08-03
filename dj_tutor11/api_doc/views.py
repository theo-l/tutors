# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-07-10 09:36:44
# @Last Modified by:   theo-l
# @Last Modified time: 2017-08-03 09:14:25

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .xviews import XView
# Create your views here.


class APIManagerView(XView):
    # model = APIInfo
    queryset = APIInfo.objects.all()
    context_object_list_name = 'objects'
    fields = '__all__'
    paginate_by = 2
    ordering = ['created_at']
    search_fields = ['endpoint']

    def get_context_data(self, **kwargs):
        """
        Insert some common context data in the template env
        """
        context = super(APIManagerView, self).get_context_data(**kwargs)
        apps = APP.enables.all()
        app_resources = []
        for app in apps:
            resources = APIInfo.enables.filter(app=app).values_list('resource_name', flat=True).distinct()
            app_resources.extend(list(resources))
        data = {'apps': apps, 'resources': app_resources}
        context.update(**data)
        return context


@csrf_exempt
def index(request, *args, **kwargs):
    queryset = APIInfo.enables.order_by('app', 'resource_name')
    context_data = kwargs or {}
    filters = kwargs or {}

    page = 1
    if request.method == 'GET':
        for key, value in request.GET.items():
            if not value:
                continue
            if key == 'page':
                page = request.GET.get('page') or page
                continue
            if key == 'q':
                search_key = value.strip(" ")
                context_data['q'] = search_key
                queryset = queryset.filter(Q(app__name__icontains=search_key) | Q(resource_name__icontains=search_key) | Q(desc__icontains=search_key))
                continue

            filters[key] = value
            context_data[key] = value

    if filters:
        print("filters:", filters)
        queryset = queryset.filter(**filters)

    paginator = Paginator(queryset.all(), 20)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    context_data.update({'objects': objects})

    print(context_data)
    return render(request, 'api_doc/index.html', context_data)


def app_resource_list(request, *args, **kwargs):
    app = APP.enables.filter(pk=kwargs['app_id']).first()
    resources = APIInfo.enables.filter(app=app).values_list('resource_name', flat=True).distinct()
    resources = Paginator(resources, 20)
    return render(request, 'api_doc/app_resource_list.html',
                  {'objects': resources, 'app': app})


def app_resource_api_list(request, *args, **kwargs):
    """
    Get all apis of the given resource of the given app
    """
    app = APP.enables.filter(pk=kwargs['app_id']).first()
    if app is None:
        return HttpResponse('Not Found')
    resource_name = kwargs['resource_name']
    apis = APIInfo.enables.filter(resource_name=resource_name).all()
    apis = Paginator(apis, 20)

    return render(request, 'api_doc/app_resource_api_list.html',
                  {'objects': apis, 'app': app, 'resource_name': resource_name})


def app_resource_api_detail(request, *args, **kwargs):
    """
    Display the api detail information
    """
    print(args, kwargs)
    api = APIInfo.enables.filter(pk=kwargs['api_id']).first()
    context_data = {
        'obj': api
    }
    return render(request, 'api_doc/app_resource_api_detail.html', context_data)

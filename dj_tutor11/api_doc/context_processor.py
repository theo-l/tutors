# -*- coding: utf-8 -*-
# @Author: theo-l
# @Date:   2017-07-11 09:18:15
# @Last Modified by:   theo-l
# @Last Modified time: 2017-07-11 16:34:33

from .models import APP, APIInfo


def api_doc_index(request, *args, **kwargs):
    """
    Generate a dict data to create the api document application's left navigation menue
    apps: {
        'app_name':{
            'app': AP_instance,
            'resources': [a list of resource name]
        }
    }
    """

    apps = APP.enables.all()
    app_resources = []
    for app in apps:
        resources = APIInfo.enables.filter(app=app).values_list('resource_name', flat=True).distinct()
        app_resources.extend(list(resources))
    data = {'apps': apps, 'resources': app_resources}
    # print("context data: ", data)
    return data

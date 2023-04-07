from django.apps import apps
from django.http import JsonResponse




def get_apps(request):
    app_configs = apps.get_app_configs()
    apps_data = []
    for app_config in app_configs:
        apps_data.append(app_config.label)
    return JsonResponse({"apps":apps_data})


def get_models(request):
    app = request.GET.get('app')
    models = []
    amodels = apps.get_models(app)
    for model in amodels:
        models.append(model.__name__)
    return JsonResponse({"models":models})


def get_model_fields(request):
    model_name = request.GET.get('model')
    app_label = request.GET.get('app')
    model_fields = []
    try:
        model = apps.get_model(app_label, model_name)
    except Exception as e:
        print(e)
        return JsonResponse({"details": str(e)}, status=500)
    
    
    try:
        fields = model._meta.get_fields()
        for field in fields:
            field_name = field.name
            field_type = field.get_internal_type()
            model_fields.append({"field": field_name, "type": field_type})
    except Exception as e:
        print(e)
        return JsonResponse({"details": str(e)}, status=500)
    return JsonResponse({"fields":model_fields})


def get_data(request):
    app_configs = apps.get_app_configs()
    apps_data = []
    from django.db import models
    data = getattr(models, "ForeignKey")
    print(data)
    for attr in vars(data):
        print(f"Attribute: {attr}, Value: {getattr(data, attr)}")

    # Loop through methods
    for method_name in dir(data):
        method = getattr(data, method_name)
        if callable(method):
            print(f"Method: {method_name}")

    for app_config in app_configs:
        print(app_config.name)
        amodels = apps.get_models(app_config)
        app_models = []
        for model in amodels:
            d = {}
            model_fields = []
            fields = model._meta.get_fields()
            for field in fields:
                field_name = field.name
                field_type = field.get_internal_type()
                model_fields.append({"field": field_name, "type": field_type})
                print("Field name:", field_name)
                print("Field type:", field_type)
            print(model.__name__)
            d["model"] =  model.__name__
            d["fields"] = model_fields
            if d not in app_models:
                app_models.append(d)
        apps_data.append({"app_label":app_config.name, "models":app_models})
    return JsonResponse({"apps":apps_data})

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from .serializers import DynamicBaseSerializer
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_datatables.renderers import DatatablesRenderer
from django.apps import apps


class DynamicModelViewSet(viewsets.ModelViewSet):
    pagination_class = DatatablesPageNumberPagination
    filter_backends = [DatatablesFilterBackend]
    serializer_class = DynamicBaseSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, DatatablesRenderer]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', {'request':self.request})
        return serializer_class(*args, **kwargs)
    

    def get_serializer_class(self):
        self.app_label = self.request.query_params.get('app')
        self.fields= tuple(self.request.query_params.getlist("fields"))
        r_model = self.request.query_params.get('model')
        self.model = apps.get_model(self.app_label, r_model)
        return self.serializer_class
    
    def get_queryset(self):
        self.app_label = self.request.query_params.get('app')
        self.fields = tuple(self.request.query_params.getlist("fields"))
        extra_filter = self.request.query_params.getlist("extra_filters", None)
        r_model = self.request.query_params.get('model')
        self.model = apps.get_model(self.app_label, r_model)
        data = self.model.objects.all()
        return data

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True,request=request)
        print(serializer.data)
        return Response(serializer.data)

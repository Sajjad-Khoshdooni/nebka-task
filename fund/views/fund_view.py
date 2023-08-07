from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from fund.models import Fund


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ('created_at', 'name', 'reg_no', 'net_asset', 'cancel_nav', 'annual_efficiency', 'investment_manager',
                  'ins_inv_no', 'ret_inv_no')


class FundListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = FundSerializer
    queryset = Fund.objects.all()

    @swagger_auto_schema(manual_parameters=[openapi.Parameter(
        name='key',
        in_=openapi.IN_QUERY,
        type=openapi.TYPE_STRING,
        description='Search funds by name (case-insensitive)',
    )])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        key = self.request.query_params.get('key')
        if key:
            return self.queryset.filter(name__icontains=key)
        return self.queryset

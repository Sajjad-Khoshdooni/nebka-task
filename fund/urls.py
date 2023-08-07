from django.urls import path

from fund.views import *

urlpatterns = [
    path('', FundListAPIView.as_view(), name='fund-list-api-view'),
]

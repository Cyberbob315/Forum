from django.conf.urls import url
from .views import ThreadSearchView

urlpatterns = [
    url(r'^search$', ThreadSearchView.as_view(), name='search'),
]

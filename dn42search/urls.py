from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from search.views import IndexView, SearchResultsView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('search', SearchResultsView.as_view(), name='results'),
    path('admin/', admin.site.urls),
]

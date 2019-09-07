from django.urls import path
from . import views

urlpatterns = [
    # в параметрах URL pattern
    # функция, которую нужно будет искать в модуле views и вызывать её
    # name - имя этого конкретного URL-маппинга
    path('', views.index, name='index'),
]
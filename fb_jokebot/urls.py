#jokebot/fb_jokebot/urls.py
from django.conf.urls import include,url
from .views import jokeview

urlpatterns=[
   url(r'^jokeboturl/?$',jokeview.as_view())
]

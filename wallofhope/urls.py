from django.urls import path
from wallofhope.views import show_wallofhope
from wallofhope.views import show_json
from wallofhope.views import add_form_ajax
from wallofhope.views import petunjuk
from wallofhope.views import post_wallofhope_flutter

app_name = 'wallofhope'

urlpatterns = [
    path('', show_wallofhope, name='show_wallofhope'),
    path('json/', show_json, name='show_json'),
    path('add/' , add_form_ajax, name='add_form_ajax'), 
    path('petunjuk/', petunjuk, name='petunjuk'),
    path('add_wallofhope/', post_wallofhope_flutter, name="post_wallofhope_flutter")
    
]
    

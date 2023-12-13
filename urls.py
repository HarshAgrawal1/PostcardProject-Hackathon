from django.urls import path
from . import views

urlpatterns = [
    path('postcard_view/', views.postcard_view, name='postcard_view'),
    # path('samplepostcard/', views.samplepostcard, name='samplepostcard'),
    path('inputform/', views.inputform, name='inputform'),
    path('send_card/', views.christmas_card, name='send_card'),
]
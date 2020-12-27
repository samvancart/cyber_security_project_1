from django.urls import path

from .views import index, signupView, addView

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signupView, name='signup'),
    path('add/', addView, name='add'),
]
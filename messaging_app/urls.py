from django.urls import path

from .views import index, signupView, addView, accountView, deleteView

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signupView, name='signup'),
    path('add/', addView, name='add'),
    path('account/<int:uid>', accountView, name='account'),
    path('delete/<int:uid>', deleteView, name='delete')
]
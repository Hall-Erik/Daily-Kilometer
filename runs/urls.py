from django.urls import path
from . import views

app_name='runs'

urlpatterns = [
    path('', views.index, name='home'),
    path('run/<int:pk>/delete/', views.DeleteRunView.as_view(), name='delete'),
]
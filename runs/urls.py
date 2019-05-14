from django.urls import path
from . import views

app_name = 'runs'

urlpatterns = [
    path('', views.index, name='home'),
    path('run/<int:pk>/', views.DetailRunView.as_view(), name='detail'),
    path('run/<int:pk>/edit/', views.UpdateRunView.as_view(), name='update'),
    path('run/<int:pk>/delete/', views.DeleteRunView.as_view(), name='delete'),

    path('gear/new', views.GearCreateView.as_view(), name='gear-create'),
    path('gear/', views.GearListView.as_view(), name='gear-list'),
    path('gear/<int:pk>/', views.GearDetailView.as_view(), name='gear-detail'),
]

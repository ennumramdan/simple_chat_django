from django.urls import path

from . import views

urlpatterns = [
    path('send_broadcast/', views.SendBroadcastView.as_view(), name='send_broadcast'),
    path('list_broadcast/', views.ListBroadcastView.as_view(), name='list_broadcast'),
    path('simple_room/', views.RoomView.as_view(), name='room'),
]
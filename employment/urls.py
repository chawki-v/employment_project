from django.urls import path
from . import views

app_name='employment'
urlpatterns = [
        path('',views.home,name='home'),
        path('register/',views.register,name='register'),
        path('profile/',views.profile,name='profile'),
        path('affiche_test/<pk>/',views.affiche_test,name='affiche_test'),
        path('activate/<uidb64>/<token>', views.activate, name='activate'),
        path('test/<pk>/',views.test,name="test"),
        ]

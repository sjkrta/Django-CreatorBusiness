from django.urls import path
from . import views

urlpatterns = [
    # accounts
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgotpassword/', views.forgotpassword_view, name='forgotpassword'),
    # creatorpanel & businesspanel
    path('', views.creatorpanel_listview, name='home'),
    path('businesspanel/', views.businesspanel_listview, name='businesspanel'),
    path('profile/<str:name>/', views.profile_view, name= 'profile'),
    path('updateprofile/', views.updateprofile_view, name= 'updateprofile'),
    # daycounter
    path('daycounter/', views.daycounter_view, name='daycounter'),
    # about
    path('about/', views.about_view, name='about'),
    # message
    path('allmessages/<str:name>/', views.message_listview, name='messagelist'),
    path('messages/<str:name>/', views.message_detailview, name='messagedetail'),
    # media
    path('media/<int:id>/', views.media_detailview, name='media'),
    path('deletepost/<int:id>/', views.deletepost, name='deletepost'),
    # filter
    path('category/<str:category>/', views.categoryfilter_listview, name='category'),
    path('tag/<str:tag>/', views.tagfilter_listview, name='tag'),
]
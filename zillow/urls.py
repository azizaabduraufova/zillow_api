from django.urls import path
from zillow import views
urlpatterns = [
    path('',views.PropertyTypeGet().as_view()),
    path('property/',views.PropertyGet().as_view()),
    path('detail_type/<int:pk>',views.PropertyTypeDetail().as_view()),
    path('detail_property/<int:pk>',views.PropertyDetail().as_view()),
    path('users/', views.UserProfileGet.as_view()),
    path('detail_users/<int:pk>/', views.UserProfileDetail.as_view())

]
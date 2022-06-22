from django.urls import path, include
from .views import LoginView, LogoutView, UserViewSet

urlpatterns = [
    path('', include('rest_framework.urls')),
    #POST credentials and login
    path('login/', LoginView.as_view()),
    #GET request to logout
    path('logout/', LogoutView.as_view()),
    #POST request to create a new user
    path('signup/', UserViewSet.as_view({
        'post': 'create',
    })),
    #get a list of users and the messages they own
    path('users/', UserViewSet.as_view({
        'get': 'list',
    })),
    path('profile/', UserViewSet.as_view({
        'get': 'retrieve',
    })),
]

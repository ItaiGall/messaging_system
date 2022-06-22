from django.urls import path
from .views import MessageViewSet

urlpatterns = [
    #GET all messages of current user
    path('', MessageViewSet.as_view({
        'get': 'list',
    })),
    # POST a new message
    path('write/', MessageViewSet.as_view({
        'post': 'create',
    })),
    #read specific message and/or delete it
    path('<str:msg_id>', MessageViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
    })),
]
'''#POST credentials and login
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
})),'''
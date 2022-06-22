from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from rest_framework import views, viewsets, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import obtain_auth_token
from .serializers import UserSerializer, LoginSerializer
from django.shortcuts import get_object_or_404

#This class allows for different permissions per method in one viewset
class ActionBasedPermission(permissions.AllowAny):
    def has_permission(self, request, view):
        for category, actions in getattr(view, 'action_permissions', {}).items():
            if view.action in actions:
                return category().has_permission(request, view)
        return False

#Decided to use APIView for Login because it has a single purpose and
# uses a distinct serializer for authentication
class LoginView(views.APIView):
    '''
    post: Login function.
    '''
    # This view should be accessible also for unauthenticated users.
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        token = obtain_auth_token
        user = serializer.validated_data['user']
        login(request, user)
        print(str(token))
        return Response(f"You logged in as {user.username}.",
                        status=status.HTTP_202_ACCEPTED)

#Same as LoginView - single purpose APIView
class LogoutView(views.APIView):
    '''
    get: Logout function:
    '''
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated,]
    def get(self, request):
        logout(request)
        return Response("You have been logged out.", status=status.HTTP_202_ACCEPTED)

#User manager with CRUD operations
class UserViewSet(viewsets.ModelViewSet):
    '''
    list: Get the user list (only when logged in as admin).
    retrieve: Get current user's profile.
    create: Register a new user.
    '''
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication, ]
    #different permissions for signup or get user-list or get user profile
    permission_classes = [ActionBasedPermission,]
    action_permissions = {
        permissions.IsAdminUser: ['list'],
        permissions.IsAuthenticated: ['retrieve'],
        permissions.AllowAny: ['create']
    }
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    #standard viewset get for user list
    #show the current user's profile
    def retrieve(self, request, *args, **kwargs):
        current_user = get_object_or_404(User, id=request.user.pk)
        serializer = UserSerializer(current_user)
        return Response("Current user profile", serializer.data, status=status.HTTP_302_FOUND)

    #sign up as new user
    def create(self, request, *args, **kwargs):
        self.permission_classes = (permissions.AllowAny,)
        serializer = UserSerializer(data=self.request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(f"You registered as {serializer.data['username']}.",
                    status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

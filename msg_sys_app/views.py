from rest_framework import viewsets, status, authentication, permissions
from rest_framework.filters import BaseFilterBackend
from rest_framework.response import Response
from rest_framework.schemas import coreapi
from .models import Message
from django.contrib.auth.models import User
from .serializers import MessageSerializer
from.slug_generator import generate_slug
from django.shortcuts import get_object_or_404
from _datetime import datetime

#To add query params in swagger
class SimpleFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        return [coreapi.coreapi.Field(
            name='msg_read',
            location='query',
            required=False,
            type='bool',
            description='Show unread messages?-Type something, show all messages?-Leave blank.',

        )]


#Message manager
class MessageViewSet(viewsets.ModelViewSet):
    '''
    list: Get a list of all messages or all unread messages.
    create: Write a new message.
    retrieve: Find a specific message by slug.
    destroy: Delete a specific message (as recipient or as author).
    ---
    '''

    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated,]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = (SimpleFilterBackend,)

    # "Get all messages -read or unread- for the logged in user or the sent messages"
    def list(self, request, *args, **kwargs):
        current_user = self.request.user.username
        is_read = bool(self.request.query_params.get('msg_read'))

        try:
            # URL for all messages of the current user: api/msg/
            if not is_read:
                messages = Message.objects.filter(recipient=current_user)
            # URL for current user's unread messages: api/msg/?msg_read=False
            else:
                messages = Message.objects.filter(recipient=current_user, msg_read=False)

            serializer = MessageSerializer(messages, many=True)
            return Response("Message list",
                            serializer.data, status=status.HTTP_200_OK)
        except:
            return Response("No messages yet",
                            status=status.HTTP_204_NO_CONTENT)

    #"Write message"
    #URL: api/create/
    def create(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            #send message only if the recipient actually exists in DB
            temp_recipient = serializer.validated_data['recipient']
            if User.objects.filter(username=temp_recipient).exists():
                slug = generate_slug()
                serializer.save(slug=slug, date_created=datetime.now(), owner=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(f"Recipient not found",status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    # "Read single message"
    #URL: api/<str:slug>/
    def retrieve(self, request, msg_id=None):
        current_user = self.request.user
        message = get_object_or_404(Message, slug=msg_id)
        # before acting, test if the message belongs to current user as recipient or as owner
        if message.recipient == current_user.username or message.owner == current_user:
            #if message belongs to current user, update its status as read message
            if message.recipient == current_user.username:
                message.msg_read = True
                message.save()
            serializer = MessageSerializer(message)
            return Response(f"Message with ID {msg_id} has been retrieved",
                            serializer.data, status=status.HTTP_302_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    #"Delete message as recipient or as owner"
    # URL: api/<str:slug>/
    def destroy(self, request, msg_id=None):
        current_user = self.request.user
        message = get_object_or_404(Message, slug=msg_id)
        #before acting, test if the message belongs to current user as recipient or as owner
        if message.recipient == current_user or message.owner == current_user:
            message.delete()
            return Response(f"Message with ID {msg_id} has been deleted",
                            status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
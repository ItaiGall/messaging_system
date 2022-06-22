from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

#Provides a list of sent messages for each user, in URL: api/users/
class CompactMessageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return f"Subject: {value.subject}, Slug: {value.slug}"

#For summarizing the users, in URL: api/users/
class UserSerializer(serializers.ModelSerializer):
    #for each owner a list of his sent messages is created
    messages = CompactMessageSerializer(many=True, read_only=True, allow_null=True)
    #For registering new users override the create method
    password = serializers.CharField(write_only=True)

    # For registering new users override the create method, URL: api/signup/
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'messages']

#providing validation during login, URL: api/login/
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
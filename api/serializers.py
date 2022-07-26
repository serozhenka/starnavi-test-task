from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers

from users.models import Account
from posts.models import Post, PostLike

class RegisterSerializer(serializers.ModelSerializer):
    """Serializer used to register a new user."""

    password = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password], style={'input_type': 'password'},
    )
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'password2']

    def create(self, validated_data):
        return Account.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return data


class LoginSerializer(serializers.Serializer):
    """Serializer used to login user."""

    email = serializers.EmailField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, required=True, style={'input_type': 'password'},
    )

    def validate(self, data):
        email, password = data.get('email'), data.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data['user'] = user
        return data

class SimpleAccountSerializer(serializers.ModelSerializer):
    """Basic account serializer that returns non-private / common fields."""

    class Meta:
        model = Account
        fields = ['username']

class PostSerializer(serializers.ModelSerializer):
    """Post serializer."""

    user = SimpleAccountSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'user', 'body', 'likes_count', 'created', 'edited_timestamp']
        read_only_fields = ['id', 'edited_timestamp']

    def create(self, validated_data):
        return Post.objects.create(
            user=self.context.get('request').user,
            body=validated_data['body'],
        )

class PostLikeSerializer(serializers.ModelSerializer):
    """Post like serializer."""

    user = SimpleAccountSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post', 'timestamp']

    def create(self, validated_data):
        return Post.objects.create(
            user=self.context.get('request').user,
            body=validated_data['body'],
        )

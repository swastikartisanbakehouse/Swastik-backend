from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number', 'whatsapp_number', 'addresses', 'is_staff', 'is_superuser', 'is_admin', 'created_at']

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number', 'whatsapp_number', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data.get('name', '')
        mobile_number = validated_data.get('mobile_number', None)
        whatsapp_number = validated_data.get('whatsapp_number', '')
        password = validated_data['password']
        
        # Use email prefix for username if not provided
        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            mobile_number=mobile_number,
            whatsapp_number=whatsapp_number
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password.')

            user = authenticate(username=email, password=password)
            if not user:
                user = authenticate(username=user_obj.username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
        else:
            raise serializers.ValidationError('Must include email and password.')

        data['user'] = user
        return data

class AdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            try:
                user_obj = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('Invalid email or password.')

            user = authenticate(username=email, password=password)
            if not user:
                user = authenticate(username=user_obj.username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            if not (user.is_staff or user.is_superuser):
                raise serializers.PermissionDenied('Access denied. Only admin users can log in here.')
        else:
            raise serializers.ValidationError('Must include email and password.')

        data['user'] = user
        return data

class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'mobile_number', 'whatsapp_number', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        name = validated_data.get('name', '')
        mobile_number = validated_data.get('mobile_number', None)
        whatsapp_number = validated_data.get('whatsapp_number', '')
        password = validated_data['password']

        username = email.split('@')[0]
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            name=name,
            mobile_number=mobile_number,
            whatsapp_number=whatsapp_number,
            is_staff=True
        )
        return user


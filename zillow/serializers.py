

from zillow.models import Property, PropertyType, Profile, ProfileType, WatchedHistory
from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import transaction


class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = ['created_at']


class PropertyTypeSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)

    class Meta:
        model = PropertyType
        fields = '__all__'


class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    first_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    last_name = serializers.CharField(max_length=30, allow_blank=True, required=False)
    email = serializers.EmailField(allow_blank=True, required=False)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=15, required=True)
    img = serializers.ImageField(allow_empty_file=True, allow_null=True, required=False)
    profile_type = serializers.SlugRelatedField(
        queryset=ProfileType.objects.all(),
        slug_field='type',
        many=True
    )

    def validate(self, attrs):
        password = attrs.get('password')
        if password:
            password_confirm = attrs.get('password_confirm')
            if not password_confirm:
                raise serializers.ValidationError({"password_confirm": "Please confirm your password."})

            if attrs['password'] != attrs['password_confirm']:
                raise serializers.ValidationError('Password and Password confirm do not match.')
        return attrs

    def create(self, validated_data):
        img = validated_data.pop('img', None)
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        phone = validated_data.pop('phone')
        profile_type = validated_data.pop('profile_type')
        with transaction.atomic():
            user = User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            profile = Profile.objects.create(user=user, phone=phone, img=img)
            profile.profile_type.set(profile_type)
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        profile = instance.profile

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        if password:
            instance.set_password(validated_data['password'])
        instance.save()

        profile.phone = validated_data.get('phone', profile.phone)
        profile.img = validated_data.get('img', profile.img)
        if 'profile_type' in validated_data:
            profile.profile_type.set(validated_data['profile_type'])
        profile.save()

        return instance

    def to_representation(self, instance):
        request = self.context.get('request')

        profile = instance.profile if hasattr(instance, 'profile') else None
        phone = profile.phone if profile else None
        img = profile.img if profile else None
        img_url = img.url if img else None

        full_img_url = request.build_absolute_uri(img_url) if request and img_url else img_url

        return {
            "id": instance.id,
            "username": instance.username,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "email": instance.email,
            "profile": {
                "id": instance.profile.id,
                "phone": phone,
                "img": full_img_url,
                "profile_type": [pt.type for pt in profile.profile_type.all()] if profile else []
            }
        }


class UserProfileTypeSerializer(serializers.ModelSerializer):
    profiles = UserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = ProfileType
        fields = '__all__'

class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            attrs['token'] = str(token.key)
            return attrs
        raise serializers.ValidationError({"message": "Invalid login/password!"})

class WatchedHistorySerializer(serializers.ModelSerializer):
    username=serializers.SerializerMethodField()
    property_title=serializers.StringRelatedField(source="property")
    class Meta:
        model = WatchedHistory
        fields =( 'id', 'watched_at', 'username', 'user', 'property', 'is_deleted', 'property_title')
        read_only_fields=('id','watched_at')
        extra_kwargs={
            "user":{"write_only":True},
            "property_title":{"write_only":True},
        }
    def get_username(self,obj):
        username=obj.user.username
        # if obj.user.first_name or obj.user.last_name:
        #     fullname=obj.user.fullname()
        return username

class PropertyStatisticsSerializer(serializers.Serializer):
    id=serializers.IntegerField(read_only=True)
    title=serializers.CharField(read_only=True)
    watched_properties_count=serializers.IntegerField(read_only=True)

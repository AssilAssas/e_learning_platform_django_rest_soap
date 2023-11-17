from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate


UserModel = get_user_model()
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['email', 'first_name', 'last_name', 'password','role']
        extra_kwargs = {'date_joind': {'required': False}}
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self,validated_data):
        user_obj = UserModel.objects.create_user(email=validated_data['email'],password=validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'],role=validated_data['role'])
                                       
        user_obj.username = 'username'
        user_obj.save()
        return user_obj
        


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_user(self, validated_data):
        email = validated_data.get('email', '')
        password = validated_data.get('password', '')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model: UserModel 
        fields = ('email','username')
        
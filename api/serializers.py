# api/serializers.py
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from .models import Product
from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegisterSerializer(RegisterSerializer):
    role = serializers.ChoiceField(choices=[('buyer', 'buyer'), ('seller', 'seller')])

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['role'] = self.validated_data.get('role', '')
        return data_dict
    

class CustomUserDetailsSerializer(UserDetailsSerializer):

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('role', 'credit')

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        #fields = ['id', 'amount_available', 'cost', 'product_name', 'seller_id']
        fields = ['id', 'amount_available', 'cost', 'product_name','seller']
        read_only_fields = ['seller']


    def create(self, validated_data):
        validated_data['seller'] = self.context['request'].user
        return super().create(validated_data)



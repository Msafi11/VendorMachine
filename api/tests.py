from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from api.models import Product
from api.models import  CustomUser,Product


class CustomUserTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password', role='buyer')
        self.seller = CustomUser.objects.create_user(username='seller', password='password', role='seller')

    def test_create_product_as_seller(self):
        self.client.force_authenticate(user=self.seller)
        url = reverse('product-list')
        data = {'product_name': 'Test Product', 'cost': 10, 'amount_available': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_product_as_buyer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product-list')
        data = {'product_name': 'Test Product', 'cost': 10, 'amount_available': 100}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Add more test cases for other endpoints...

class ProductTests(APITestCase):
    def setUp(self):
        self.seller = CustomUser.objects.create_user(username='seller', password='password', role='seller')
        self.product = Product.objects.create(product_name='Test Product', cost=10, amount_available=100, seller=self.seller)

    def test_retrieve_product(self):
        self.client.force_authenticate(user=self.seller) 
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], 'Test Product')

class DepositTests(APITestCase):
    def setUp(self):
        self.buyer = CustomUser.objects.create_user(username='buyer', password='password', role='buyer')

    def test_deposit_coins_as_seller(self):
        self.seller = CustomUser.objects.create_user(username='seller', password='password', role='seller')
        self.client.force_authenticate(user=self.seller)
        url = reverse('deposit')
        data = {'amount': 10}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class ResetDepositTests(APITestCase):
    def setUp(self):
        self.buyer = CustomUser.objects.create_user(username='buyer', password='password', role='buyer')

    def test_reset_deposit_as_buyer(self):
        self.client.force_authenticate(user=self.buyer)
        url = reverse('reset')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_deposit_as_seller(self):
        self.seller = CustomUser.objects.create_user(username='seller', password='password', role='seller')
        self.client.force_authenticate(user=self.seller)
        url = reverse('reset')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
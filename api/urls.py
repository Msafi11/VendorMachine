# api/urls.py

from django.urls import path, include
from api.views import CustomUserView, ProductViewSet, DepositView, BuyView, ResetDepositView, CustomRegisterView

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
    path('signup/', CustomRegisterView.as_view(), name='rest_register'),
    path('users/', CustomUserView.as_view()),
    path('users/<int:pk>/', CustomUserView.as_view()),
    path('products/', ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-list'),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-detail'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('buy/', BuyView.as_view(), name='buy'),
    path('reset/', ResetDepositView.as_view(), name='reset'),
]

# path('signup/', include('dj_rest_auth.registration.urls')),

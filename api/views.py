# api/views.py

from rest_framework import viewsets
from api.models import CustomUser, Product
from api.serializers import ProductSerializer, CustomUserDetailsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.registration.views import RegisterView
import logging
from .signals import deposit_made, buy_made, reset_deposit_made, product_added, product_updated , product_deleted

logger = logging.getLogger('user_actions')


class CustomUserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserDetailsSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))
        user.delete()

        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


    
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        if not request.user.role == 'seller':
            return Response({"error": "Only sellers can create products."},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()  # Automatically assigns the logged-in user as the seller
            product_added.send(sender=None, user=request.user,product=serializer.save())
            logger.info(f"Seller {request.user.username} added {serializer.save().amount_available} of {serializer.save().product_name} costs {serializer.save().cost} ")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            
            if request.user != product.seller:
                return Response({"error": "Only the seller of this product can update it."},
                                status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            product_updated.send(sender=None, user=request.user,product=serializer.save())
            logger.info(f"Seller {request.user.username} updated the product with id: {serializer.save().id} to: {serializer.save().product_name} costs: {serializer.save().cost} amount available: {serializer.save().amount_available} ")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        product = self.get_object(pk)
        # Ensure the current user is the seller of the product
        if request.user != product.seller:
            return Response({"error": "Only the seller of this product can delete it."},
                            status=status.HTTP_403_FORBIDDEN)
        product.delete()
        product_deleted.send(sender=None, user=request.user,product=product)
        logger.info(f"Seller {request.user.username} deleted the {product.product_name}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        queryset = Product.objects.all()
        return get_object_or_404(queryset, pk=pk)


class DepositView(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'buyer':
            return Response({"error": "Only users with the 'buyer' role can deposit coins."},
                            status=status.HTTP_403_FORBIDDEN)

        amount = request.data.get('amount')
        if amount not in [5, 10, 20, 50, 100]:
            return Response({"error": "Invalid coin amount. Must be 5, 10, 20, 50, or 100."},
                            status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.credit += amount
        user.save()

        deposit_made.send(sender=None, user=user, amount=amount)

        logger.info(f"Buyer {user.username} made a deposit of {amount} coins")

        return Response({"message": f"Successfully deposited {amount} cent coins into your vending machine account."},
                        status=status.HTTP_200_OK)
    


class BuyView(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'buyer':
            return Response({"error": "Only users with the 'buyer' role can buy products."},
                            status=status.HTTP_403_FORBIDDEN)

        product_id = request.data.get('productId')
        amount = int(request.data.get('amount'))

        if not (product_id and amount):
            return Response({"error": "Please provide both productId and amount."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid product ID."},
                            status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Amount must be greater than zero."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if amount > product.amount_available:
            return Response({"error": "Insufficient stock to fulfill the request."},
                            status=status.HTTP_400_BAD_REQUEST)

        total_spent = product.cost * amount

        if request.user.credit < total_spent:
            return Response({"error": "Insufficient credit to make the purchase."},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.credit -= total_spent
        request.user.save()

        product.amount_available -= amount
        product.save()

        seller = product.seller
        seller.credit += total_spent
        seller.save()
        
        


        response_data = {
            "total_spent": total_spent,
            "products_purchased": {
                "product_id": product.id,
                "product_name": product.product_name,
                "amount": amount
            },
            "change": request.user.credit
        }
        buy_made.send(sender=None, user=request.user, amount=amount)

        logger.info(f"Buyer {request.user.username} made a purchase of {amount} {product.product_name} and paid {total_spent}")
        
        
        
        return Response(response_data, status=status.HTTP_200_OK)
    

class ResetDepositView(APIView):
    def post(self, request):
        if not request.user.is_authenticated or request.user.role != 'buyer':
            return Response({"error": "Only users with the 'buyer' role can reset their deposit."},
                            status=status.HTTP_403_FORBIDDEN)

        request.user.credit = 0
        request.user.save()

        reset_deposit_made.send(sender=None, user=request.user)

        logger.info(f"Buyer {request.user.username} has reset his credit")

        return Response({"message": "Deposit reset successfully."},
                        status=status.HTTP_200_OK)
    

class CustomRegisterView(RegisterView):
    def post(self, request, *args, **kwargs):
        # Call the parent post method to perform the sign-up logic
        response = super().post(request, *args, **kwargs)
        

        return response
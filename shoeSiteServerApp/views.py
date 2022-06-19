from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shoe, Comment, Customer, Category, CartDetail, Stock, Sale, SaleDetail
from .serializers import ShoeSerializer, CustomerSerializer, CartDetailSerializer, SaleSerializer, SaleDetailSerializer, CommentSerializer, \
    CategorySerializer, CustomerDisplaySerializer, AddCartDetailSerializer
from rest_framework import generics, viewsets, mixins, status, authentication, permissions
from rest_framework.views import APIView
from .permissions import IsOwner


class ShoeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shoe.objects.all()
    serializer_class = ShoeSerializer


class CustomerView(viewsets.ReadOnlyModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerDisplaySerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated,
                          IsOwner]

    # permission_map = {
    #     "get_own_data": [permissions.IsAuthenticated]
    # }
    #
    # def get_permissions(self):
    #     return [permission() for permission in self.permission_map.get(self.action, self.permission_classes)]

    @action(detail=False, methods=['get'])
    def get_own_data(self, request, pk=None):
        user = request.user
        customer_qs = Customer.objects.filter(user=user)
        if customer_qs.exists():
            customer = customer_qs.first()
            serializer = CustomerDisplaySerializer(customer)
            return Response(data=serializer.data)
        return Response({"detail": "Invalid customer"}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    def post(self, request, format=None):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response("Create success", status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartDetailViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = CartDetail.objects.filter(customer__user=request.user)
        serializer = CartDetailSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            qty = request.data.get('qty')
            stock_id = request.data.get('stock')
            stock = Stock.objects.get(pk=stock_id)
            request.data['customer'] = request.user.customer.id
            serializer = AddCartDetailSerializer(data=request.data)
            if serializer.is_valid() and stock.qty >= qty:
                print('in')
                serializer.save()
                return Response("Create success", status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        try:
            instance = CartDetail.objects.get(pk=pk)
            qty = int(request.data.get("qty"))
            stock = Stock.objects.get(pk=instance.stock.id)
            if qty <= stock.qty:
                instance.qty = qty
                instance.save()
                return Response("Success")
            return Response("Out of stocks", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            instance = CartDetail.objects.get(pk=pk)
            instance.delete()
            return Response("Delete success", status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CommentCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class SaleViewSet(viewsets.ViewSet):
    def list(self, request):
        # queryset = Sale.objects.filter(customer__user=request.user)
        queryset = request.user.customer.sales.all()
        serializer = SaleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        try:
            sale = Sale(customer=request.user.customer)
            cardDetails = CartDetail.objects.filter(
                customer__user=request.user)

            # check out of stock
            for cartDetail in cardDetails:
                if cartDetail.stock.qty < cartDetail.qty:
                    return Response("Out of stock", status=status.HTTP_400_BAD_REQUEST)
            # calculate price and sub qty on stock
            sale.save()
            total = 0
            for cartDetail in cardDetails:
                stock = cartDetail.stock
                SaleDetail.objects.create(
                    stock=stock, qty=cartDetail.qty, sale=sale)
                stock.qty -= cartDetail.qty
                stock.save()
                total += cartDetail.qty*stock.shoe.price
                cartDetail.delete()
            sale.total = total
            sale.save()
            serializer = SaleSerializer(sale)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(e, status=status.HTTP_400_BAD_REQUEST)

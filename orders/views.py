from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from inventory.models import Inventory


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "draft":
            return Response({"error": "Only draft orders can be confirmed"})

        items = OrderItem.objects.filter(order=order)

        with transaction.atomic():

            for item in items:

                inventory = Inventory.objects.get(product=item.product)

                if inventory.quantity < item.quantity:
                    return Response({
                        "error": f"Insufficient stock for {item.product.name}"
                    })

            for item in items:

                inventory = Inventory.objects.get(product=item.product)

                inventory.quantity -= item.quantity
                inventory.save()

        # confirm order
        order.status = "confirmed"
        order.save()

        return Response({"message": "Order confirmed successfully"})


    @action(detail=True, methods=['post'])
    def deliver(self, request, pk=None):

        order = self.get_object()

        if order.status.lower() != "confirmed":
            return Response({"error": "Only confirmed orders can be delivered"})

        order.status = "delivered"
        order.save()

        return Response({"message": "Order delivered successfully"})


class OrderItemViewSet(viewsets.ModelViewSet):

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
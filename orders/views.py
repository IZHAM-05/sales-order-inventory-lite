from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from .models import Order
from .serializers import OrderSerializer, OrderItemSerializer,PlaceOrderSerializer
from inventory.models import Inventory
from datetime import datetime
import random
from .models import OrderItem

class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):

        order = self.get_object()

        if order.status != "draft":
            return Response(
                {"error": "Only draft orders can be confirmed"},
                status=400
            )

        items = order.items.all()

        total = 0   # <-- ADD THIS

        with transaction.atomic():

            for item in items:

                inventory = Inventory.objects.select_for_update().get(
                    product=item.product
                )

                if inventory.quantity < item.quantity:
                    return Response(
                        {
                           "error": f"Insufficient stock for {item.product.name}. Available: {inventory.quantity}, Requested: {item.quantity}"
                        },
                        status=400
                    )

                inventory.quantity -= item.quantity
                inventory.save()

                total += item.line_total   # <-- ADD THIS

            order.total_amount = total   # <-- ADD THIS
            order.status = "confirmed"
            order.save()

        return Response(
            {"message": "Order confirmed successfully"}
        )


    @action(detail=True, methods=["post"])
    def deliver(self, request, pk=None):

        order = self.get_object()

        if order.status != "confirmed":
            return Response(
                {"error": "Only confirmed orders can be delivered"},
                status=400
            )

        order.status = "delivered"
        order.save()

        return Response(
            {"message": "Order delivered successfully"}
        )
    
    @action(detail=False, methods=["post"], serializer_class=PlaceOrderSerializer)
    def place_order(self, request):

        serializer = PlaceOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dealer = serializer.validated_data["dealer"]
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        from datetime import datetime
        import random
        from .models import OrderItem

        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000,9999)}"

        order = Order.objects.create(
            dealer=dealer,
            order_number=order_number,
            status="draft"
        )

        unit_price = product.price
        line_total = unit_price * quantity

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=unit_price,
            line_total=line_total
        )

        order.total_amount = line_total
        order.save()

        return Response({
            "message": "Order created successfully",
            "order_id": order.id
        })
    
    
    def update(self, request, *args, **kwargs):
        order = self.get_object()

        if order.status != "draft":
            return Response(
                {"error": "Only draft orders can be edited"},
                status=400
            )

        return super().update(request, *args, **kwargs)
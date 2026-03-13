from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
from inventory.models import Inventory
from dealers.models import Dealer
from django.db import transaction
import random
from datetime import datetime


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "dealer",
            "order_number",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
            "items"
        ]

        read_only_fields = [
            "order_number",
            "status",
            "total_amount",
            "created_at",
            "updated_at"
        ]


    def create(self, validated_data):

        items_data = validated_data.pop("items")

        today = datetime.now().strftime("%Y%m%d")
        random_number = random.randint(1000, 9999)

        order_number = f"ORD-{today}-{random_number}"

        order = Order.objects.create(
            order_number=order_number,
            status="draft",
            total_amount=0,
            **validated_data
        )

        total_amount = 0

        for item in items_data:

            product = item["product"]
            quantity = item["quantity"]

            inventory = Inventory.objects.get(product=product)

            if inventory.quantity < quantity:
                raise serializers.ValidationError(
                    f"Insufficient stock for {product.name}"
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

            total_amount += line_total

        order.total_amount = total_amount
        order.save()

        return order
    

    def validate(self, data):

        if not self.initial_data.get("items"):
            raise serializers.ValidationError("Order must contain at least one item")

        return data


    def update(self, instance, validated_data):
        # 1. Pop the nested items data
        items_data = validated_data.pop('items', None)

        # 2. Update the Order fields (like dealer, status, etc.)
        # Using 'dealer' instead of 'customer'
        instance.dealer = validated_data.get('dealer', instance.dealer)
        instance.status = validated_data.get('status', instance.status)
        instance.order_number = validated_data.get('order_number', instance.order_number)
        instance.save()

        # 3. Handle nested OrderItems
        if items_data is not None:
            # Simple approach: clear old items and add new ones
            instance.items.all().delete()
            for item_data in items_data:
                OrderItem.objects.create(order=instance, **item_data)
            
            # Optional: Recalculate total_amount here if needed
                
        return instance



    
class PlaceOrderSerializer(serializers.Serializer):
    

    dealer = serializers.PrimaryKeyRelatedField(queryset=Dealer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance and instance.get("product"):
            representation["price"] = instance["product"].price

        return representation
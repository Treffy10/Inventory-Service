from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer, OrderItemEventSerializer
import inventario.events as events


@api_view(["POST"])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET"])
def list_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


# Aquí llegan los eventos desde OrderService
@api_view(["POST"])
def order_created_event(request):
    serializer = OrderItemEventSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    data = serializer.validated_data
    product_id = data["IdProduct"]
    qty = data["Quantity"]

    try:
        product = Product.objects.get(IdProduct=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # Validar stock
    if product.CurrentStock < qty:
        events.emit_stock_insufficient(product_id)
        return Response({"error": "Stock insuficiente"}, status=400)

    # Actualizar stock
    product.CurrentStock -= qty
    product.save()

    events.emit_stock_updated(product_id, product.CurrentStock)

    return Response({"message": "Stock actualizado"})

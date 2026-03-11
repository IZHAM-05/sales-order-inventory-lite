from rest_framework import viewsets
from .models import Dealer
from .serializers import DealerSerializer


class DealerViewSet(viewsets.ModelViewSet):

    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
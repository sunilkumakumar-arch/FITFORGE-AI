from django.db.models import Sum

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment
from .serializers import PaymentSerializer




class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.select_related(
        "member",
        "membership_plan",
    )

    serializer_class = PaymentSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            data=request.data
        )

        if not serializer.is_valid():

            print("PAYMENT ERRORS:")
            print(serializer.errors)

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        payment = serializer.save()

        

        return Response(
            PaymentSerializer(payment).data,
            status=status.HTTP_201_CREATED
        )
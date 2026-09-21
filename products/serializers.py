from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ["id","name","length","width","height","weight","created_at",]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        dimensions = [
            attrs["length"],
            attrs["width"],
            attrs["height"],
            attrs["weight"],
        ]

        if any(value <= 0 for value in dimensions):
            raise serializers.ValidationError(
                "Dimensions and weight must be greater than zero."
            )

        return attrs
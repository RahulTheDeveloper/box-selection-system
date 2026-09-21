from rest_framework import serializers

from .models import Box


class BoxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Box
        fields = [
            "id",
            "name",
            "length",
            "width",
            "height",
            "max_weight",
            "cost",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        dimensions = [
            attrs["length"],
            attrs["width"],
            attrs["height"],
            attrs["max_weight"],
            attrs["cost"],
        ]

        if any(value <= 0 for value in dimensions):
            raise serializers.ValidationError(
                "Dimensions, max weight and cost must be greater than zero."
            )

        return attrs
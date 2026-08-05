from rest_framework import serializers

from workouts.models import (
    Exercise,
    ExerciseCategory,
    Equipment,
    MuscleGroup,
    ExerciseMedia,
)


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = "__all__"


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class ExerciseMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseMedia
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):

    muscle_group_name = serializers.CharField(
        source="muscle_group.name",
        read_only=True,
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )

    equipment_name = serializers.CharField(
        source="equipment.name",
        read_only=True,
        allow_null=True,
    )

    class Meta:
        model = Exercise
        fields = "__all__"
from django.db import models


class MuscleGroup(models.Model):
    """
    Primary muscle groups.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=1,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class ExerciseCategory(models.Model):
    """
    Push / Pull / Legs / Cardio etc.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Equipment(models.Model):
    """
    Equipment master.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Exercise(models.Model):

    DIFFICULTY_CHOICES = [
        ("BEGINNER", "Beginner"),
        ("INTERMEDIATE", "Intermediate"),
        ("ADVANCED", "Advanced"),
    ]

    name = models.CharField(
        max_length=150,
        unique=True,
    )

    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.PROTECT,
        related_name="exercises",
    )

    category = models.ForeignKey(
        ExerciseCategory,
        on_delete=models.PROTECT,
        related_name="exercises",
    )

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="exercises",
    )

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default="BEGINNER",
    )

    instructions = models.TextField()

    description = models.TextField(
        blank=True,
    )

    primary_muscles = models.TextField(
        blank=True,
    )

    secondary_muscles = models.TextField(
        blank=True,
    )

    calories_factor = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.00,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ExerciseMedia(models.Model):

    MEDIA_TYPES = [
        ("IMAGE", "Image"),
        ("VIDEO", "Video"),
    ]

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="media",
    )

    media_type = models.CharField(
        max_length=20,
        choices=MEDIA_TYPES,
    )

    file = models.FileField(
        upload_to="exercise_media/",
    )

    caption = models.CharField(
        max_length=255,
        blank=True,
    )

    display_order = models.PositiveIntegerField(
        default=1,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.exercise.name} - {self.media_type}"
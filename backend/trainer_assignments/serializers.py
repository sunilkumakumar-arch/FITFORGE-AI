from rest_framework import serializers

from .models import TrainerAssignment
from trainers.models import TrainerWeeklyOff


class TrainerAssignmentSerializer(
    serializers.ModelSerializer
):

    trainer_name = serializers.CharField(
        source="trainer.first_name",
        read_only=True
    )

    member_name = serializers.CharField(
        source="member.first_name",
        read_only=True
    )

    class Meta:
        model = TrainerAssignment
        fields = "__all__"

    def validate(self, attrs):

        trainer = attrs.get("trainer")
        slot_time = attrs.get("slot_time")
        day_pattern = attrs.get("day_pattern")
        goal_type = attrs.get("goal_type")
        package_type = attrs.get("package_type")

        if not trainer:
            return attrs

        # -------------------------------------------------
        # CHECK 1 : TRAINER MUST BE AVAILABLE
        # -------------------------------------------------

        if not trainer.available_for_pt:
            raise serializers.ValidationError(
                "Selected trainer is not available for PT."
            )

        if trainer.employment_status != "Active":
            raise serializers.ValidationError(
                "Selected trainer is not active."
            )

        # -------------------------------------------------
        # CHECK 2 : WEEKLY OFF VALIDATION
        # -------------------------------------------------

        weekly_off = (
            TrainerWeeklyOff.objects
            .filter(trainer=trainer)
            .order_by("-week_start_date")
            .first()
        )

        if weekly_off:

            off_day = weekly_off.off_day

            if (
                day_pattern == "MWF" and
                off_day in [
                    "Monday",
                    "Wednesday",
                    "Friday"
                ]
            ):
                raise serializers.ValidationError(
                    f"Trainer weekly off is {off_day}. MWF slot cannot be assigned."
                )

            if (
                day_pattern == "TTS" and
                off_day in [
                    "Tuesday",
                    "Thursday",
                    "Saturday"
                ]
            ):
                raise serializers.ValidationError(
                    f"Trainer weekly off is {off_day}. TTS slot cannot be assigned."
                )

       # -------------------------------------------------
       # CHECK 3 : SLOT CAPACITY LOGIC
       # -------------------------------------------------

        existing_assignments = (
            TrainerAssignment.objects
            .filter(
                trainer=trainer,
                slot_time=slot_time,
                is_active=True,
            )
        )

        # 6 DAYS PACKAGE

        if package_type == "6_DAYS":

            six_day_count = (
                existing_assignments
                .filter(package_type="6_DAYS")
                .count()
            )

            if six_day_count >= 2:
                raise serializers.ValidationError(
                    "Selected trainer slot is full."
                )

        # 3 DAYS PACKAGE

        else:

            same_pattern_count = (
               existing_assignments
               .filter(
                   package_type="3_DAYS",
                   day_pattern=day_pattern
                )
                .count()
            )

            if same_pattern_count >= 2:
                raise serializers.ValidationError(
                    f"{day_pattern} slot is full."
                )
        # -------------------------------------------------
        # CHECK 4 : GOAL COMPATIBILITY
        # -------------------------------------------------

        existing_goals = set(
            existing_assignments.values_list(
                "goal_type",
                flat=True
            )
        )

        existing_goals.discard(None)

        if existing_goals:

            if len(existing_goals) > 1:
                raise serializers.ValidationError(
                    "Trainer slot has conflicting goals. Contact administrator."
                )

            slot_goal = list(existing_goals)[0]

            if slot_goal != goal_type:
                raise serializers.ValidationError(
                    f"This slot is already reserved for {slot_goal}. Different goals cannot share the same trainer slot."
                )

        # -------------------------------------------------
        # CHECK 5 : PACKAGE CONFLICT LOGIC
        # -------------------------------------------------

        same_slot_assignments = (
            TrainerAssignment.objects.filter(
                trainer=trainer,
                slot_time=slot_time,
                is_active=True,
            )
        )

        existing_6_day = same_slot_assignments.filter(
            package_type="6_DAYS"
        ).exists()

        existing_3_day = same_slot_assignments.filter(
            package_type="3_DAYS"
        ).exists()

        # New 6 day assignment

        if package_type == "6_DAYS":

            if existing_3_day:
                raise serializers.ValidationError(
                    "Cannot assign 6-day package. 3-day clients already occupy this slot."
                )

        # New 3 day assignment

        if package_type == "3_DAYS":

           if existing_6_day:
               raise serializers.ValidationError(
                   "Cannot assign 3-day package. A 6-day client already occupies this slot."
                )
        return attrs 
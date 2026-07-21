from trainers.models import Trainer
from .models import TrainerAssignment


class TrainerAssignmentService:
    """
    Handles all Trainer Assignment business logic.

    Responsibilities:
    - Find available trainers
    - Auto assign trainer
    - Create trainer assignments
    - Change trainer
    """

    @staticmethod
    def is_trainer_available_for_time(trainer, slot_time):
        """
        Returns True if the trainer works during the requested slot.
        """

        if not slot_time:
            return False

        try:
            parts = str(slot_time).split(":")

            hour = int(parts[0])
            minute = int(parts[1])

            total_minutes = (hour * 60) + minute

        except Exception:
            return False

        shift_map = {

            "SHIFT_1": [
                (360, 630),      # 6:00 - 10:30
                (1020, 1290),    # 17:00 - 21:30
            ],

            "SHIFT_2": [
                (360, 630),
                (1050, 1320),
            ],

            "SHIFT_3": [
                (360, 900),
            ],

            "SHIFT_4": [
                (780, 1320),
            ],

            "SHIFT_5": [
                (330, 930),
            ],

            "SHIFT_6": [
                (720, 1260),
            ],
        }

        shifts = shift_map.get(
            trainer.shift_type,
            []
        )

        for start, end in shifts:

            if start <= total_minutes <= end:
                return True

        return False

    @staticmethod
    def get_active_membership_count(trainer):
        """
        Returns active membership count of trainer.
        """

        return TrainerAssignment.objects.filter(
            trainer=trainer,
            assignment_type="MEMBERSHIP",
            is_active=True,
        ).count()

    @staticmethod
    def get_pt_assignments(trainer, slot_time):
        """
        Returns active PT assignments for trainer in slot.
        """

        return TrainerAssignment.objects.filter(
            trainer=trainer,
            slot_time=slot_time,
            assignment_type="PT",
            is_active=True,
        )

    @staticmethod
    def get_available_trainers(goal_type, slot_time):
        """
        Returns all trainers available for the requested slot.
        """

        available_trainers = []

        trainers = Trainer.objects.filter(
            employment_status="Active",
            available_for_pt=True,
        )

        print("\n========== AVAILABLE TRAINERS ==========")
        print(f"Goal Type : {goal_type}")
        print(f"Slot Time : {slot_time}")
        print(f"Total Trainers : {trainers.count()}")

        for trainer in trainers:

            print("\n----------------------------------------")
            print(f"Checking Trainer : {trainer.first_name} {trainer.last_name}")

            # ----------------------------------
            # Membership Capacity
            # ----------------------------------

            current_members = (
                TrainerAssignmentService.get_active_membership_count(
                  trainer
                )
            )

            print(
                f"Members : {current_members}/{trainer.trainer_capacity}"
            )

            if current_members >= trainer.trainer_capacity:
                print("Rejected : Trainer capacity full")
                continue

            # ----------------------------------
            # Shift Availability
            # ----------------------------------

            if not TrainerAssignmentService.is_trainer_available_for_time(
                trainer,
               slot_time,
            ):
                print(
                    f"Rejected : Shift mismatch ({trainer.shift_type})"
                )
                continue

            print("Shift : OK")

            # ----------------------------------
            # PT Slot Capacity
            # ----------------------------------

            current_assignments = (
                TrainerAssignmentService.get_pt_assignments(
                    trainer,
                    slot_time,
                )
            )

            pt_count = current_assignments.count()

            print(f"PT Clients : {pt_count}/2")

            if pt_count >= 2:
                print("Rejected : PT slot full")
                continue

            # ----------------------------------
            # Goal Compatibility
            # ----------------------------------

            existing_goals = set(
                current_assignments.values_list(
                    "goal_type",
                     flat=True,
                )
            )

            existing_goals.discard(None)

            if existing_goals:

                existing_goal = list(existing_goals)[0]

                if existing_goal != goal_type:

                    print(
                        f"Rejected : Goal mismatch ({existing_goal})"
                    )  

                    continue

            print("Goal : OK")

            # ----------------------------------
            # Available
            # ----------------------------------

            available_trainers.append({
                "id": trainer.id,
                "trainer_code": trainer.trainer_code,
                "trainer_name": f"{trainer.first_name} {trainer.last_name}",
                "trainer_level": trainer.trainer_level,
                "rating": trainer.rating,
                "experience_years": trainer.experience_years,
                "specialization": trainer.specialization,
                "shift_type": trainer.shift_type,
                "trainer_capacity": trainer.trainer_capacity,
                "current_members": current_members,
                "active_clients": pt_count,
                "available_slots": max(0, 2 - pt_count),
            })

            print("Accepted")

        available_trainers.sort(
            key=lambda x: (
                x["active_clients"],
                -float(x["rating"]),
            )
        )

        print(
            f"\nAvailable Trainers : {len(available_trainers)}"
        )

        return available_trainers

    @staticmethod
    def auto_assign_trainer(goal_type, slot_time):
        """
        Auto assigns the best trainer.

        Will be implemented
        in Step 3.
        """

        return None

    @staticmethod
    def create_assignment(data):
        """
        Creates trainer assignment.

        Will be implemented
        in Step 4.
        """

        raise NotImplementedError()

    @staticmethod
    def change_trainer(data):
        """
        Changes trainer.

        Will be implemented
        in Step 5.
        """

        raise NotImplementedError()
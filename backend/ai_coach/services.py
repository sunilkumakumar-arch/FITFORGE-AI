from datetime import datetime


class WorkoutGeneratorService:

    @staticmethod
    def generate(
        goal,
        experience,
        days_per_week,
    ):

        if goal == "MUSCLE_GAIN":

            return {
                "goal": goal,
                "split": "Push Pull Legs",
                "days": [
                    {
                        "day": 1,
                        "focus": "Push",
                        "exercises": [
                            "Bench Press",
                            "Incline Dumbbell Press",
                            "Shoulder Press",
                            "Lateral Raise",
                            "Tricep Pushdown",
                        ],
                    },
                    {
                        "day": 2,
                        "focus": "Pull",
                        "exercises": [
                            "Deadlift",
                            "Lat Pulldown",
                            "Barbell Row",
                            "Face Pull",
                            "Bicep Curl",
                        ],
                    },
                    {
                        "day": 3,
                        "focus": "Legs",
                        "exercises": [
                            "Squat",
                            "Leg Press",
                            "Romanian Deadlift",
                            "Leg Curl",
                            "Calf Raise",
                        ],
                    },
                ],
                "generated_at": str(datetime.now()),
            }

        if goal == "WEIGHT_LOSS":

            return {
                "goal": goal,
                "split": "Full Body",
                "days": [
                    {
                        "day": 1,
                        "focus": "Full Body",
                        "cardio": "20 min incline walk",
                    },
                    {
                        "day": 2,
                        "focus": "Full Body",
                        "cardio": "20 min cycling",
                    },
                    {
                        "day": 3,
                        "focus": "Full Body",
                        "cardio": "20 min rowing",
                    },
                ],
                "generated_at": str(datetime.now()),
            }

        return {
            "goal": goal,
            "message": "Workout generated",
            "generated_at": str(datetime.now()),
        }


class PostureAssessmentService:

    @staticmethod
    def analyze():

        return {
            "issues": [
                "Forward Head Posture",
                "Rounded Shoulders",
            ],
            "corrective_exercises": [
                "Chin Tucks",
                "Wall Slides",
                "Band Pull Aparts",
            ],
        }
    
class NutritionGeneratorService:

    @staticmethod
    def generate(
        weight,
        height,
        age,
        goal,
    ):

        calories = weight * 30

        protein = round(weight * 2)

        carbs = round(weight * 4)

        fats = round(weight * 0.8)

        return {
            "goal": goal,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fats": fats,
        }    
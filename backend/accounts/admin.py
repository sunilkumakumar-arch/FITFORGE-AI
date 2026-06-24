


from django.contrib import admin
from .models import UserProfile, Trainer , Membership , Payment , Attendance

admin.site.register(UserProfile)
admin.site.register(Trainer)
admin.site.register(Membership)
admin.site.register(Payment)
admin.site.register(Attendance)

from .models import (
    UserProfile,
    Trainer,
    Membership,
    Payment,
    Attendance,
    WorkoutPlan
)

admin.site.register(WorkoutPlan)



from .models import DietPlan
admin.site.register(DietPlan)



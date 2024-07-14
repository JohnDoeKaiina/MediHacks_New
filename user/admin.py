from django.contrib import admin
from .models import User, Prescrition, MoodTracker


admin.site.register(User)
admin.site.register(Prescrition)
admin.site.register(MoodTracker)
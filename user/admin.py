from django.contrib import admin
from user.models import Users, Questions, Dispatchs, Subscriptions

admin.site.register(Users)
admin.site.register(Questions)
admin.site.register(Dispatchs)
admin.site.register(Subscriptions)

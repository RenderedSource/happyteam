from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from garbagecollector.models import MacAddress, GcLoosers, Room, Seat

class MacAddressInline(admin.StackedInline):
    model = MacAddress
    extra = 1

class UserAdmin(UserAdmin):
    inlines = [MacAddressInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class GcLoosersAdmin(admin.ModelAdmin):
    pass

admin.site.register(GcLoosers, GcLoosersAdmin)

class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Room, RoomAdmin)

class SeatAdmin(admin.ModelAdmin):
    pass
admin.site.register(Seat, SeatAdmin)

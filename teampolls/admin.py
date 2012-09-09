#-*- coding: utf-8 -*-
from django.contrib import admin
from teampolls.models import Poll, PollVariant, UserAnswer


class PollVariantInline(admin.TabularInline):
    model = PollVariant
    fk_name = "poll"

class PollAdmin(admin.ModelAdmin):
    inlines = [
        PollVariantInline
    ]

admin.site.register(Poll, PollAdmin)

class UserAnswerAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserAnswer, UserAnswerAdmin)

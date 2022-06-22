from django.contrib import admin
from .models import Message
from datetime import datetime

#decided to arrange fields in a certain way in django-admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_created', 'recipient', 'owner')
    list_filter = ('date_created', 'owner', 'recipient')
    search_fields = ('owner', 'recipient')
    fields = (('id', 'slug'), ('owner', 'recipient'), 'subject', 'message', 'date_created', 'msg_read')
    readonly_fields = ('id', 'slug', 'owner', 'date_created', 'msg_read')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user.username
        obj.date_created = datetime.now()
        obj.save()

admin.site.register(Message, MessageAdmin)

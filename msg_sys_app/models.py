from django.db import models

class Message(models.Model):
    #I decided to add an auto-generated slug in order not to expose the unique ID
    #I decided against an AutoSlugField because I aimed for a random 4 letter slug
    slug = models.CharField(max_length=30, editable=False, unique=False, null=False, blank=False)
    #I decided to use the boiler-plate Django User model
    owner = models.ForeignKey('auth.User', related_name='messages', editable=False, null=True, blank=False, on_delete=models.CASCADE)
    #I decided to assume a relatively short list of users, therefore recipient menu
    recipient = models.CharField(max_length=30, null=False, blank=False, verbose_name='recipient(username)')
    #Subject and message are the main fields to be edited
    subject = models.CharField(max_length=40, null=True, blank=False)
    message = models.TextField(blank=False, null=True)
    #datetime won't be editable
    date_created = models.DateTimeField(editable=False, blank=False, null=False)
    #A boolean field to indicate whether the message has been read at least once:
    msg_read = models.BooleanField(editable=False, default=False, blank=False)

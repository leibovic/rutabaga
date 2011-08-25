from django.db import models
from django.contrib.auth.models import User

STATUS = (
  (0, 'Active'),
  (1, 'Alum'),
  (2, 'New Member'),
  (3, 'PRC')
)

class Residence(models.Model):
  name = models.CharField(max_length=100)

  def __unicode__(self):
    return unicode(self.name)

class Sister(models.Model):
  user = models.ForeignKey(User, unique=True)
  class_year = models.IntegerField()
  status = models.IntegerField(choices=STATUS)
  photo_url = models.CharField(max_length=100, blank=True)

  residence = models.ForeignKey(Residence, null=True)
  phone_number = models.CharField(max_length=10, blank=True)

  hometown = models.CharField(max_length=100, blank=True)
  bio = models.TextField(blank=True)
  interests = models.TextField(blank=True)

  def full_name(self):
    return "%s %s" % (self.user.first_name, self.user.last_name)
  full_name.short_description = 'Name'

  def __unicode__(self):
    return unicode("%s %s" % (self.user.first_name, self.user.last_name))

class Event(models.Model):
  name = models.CharField(max_length=100)
  date = models.DateField()
  points = models.IntegerField()

  # The sisters who were at the event
  sisters = models.ManyToManyField(Sister, blank=True)

  def __unicode__(self):
    return unicode("%s (%s)" % (self.name, self.date))

class Content(models.Model):
  # The name of the view function that will use this content.
  view = models.CharField(max_length=100)

  html = models.TextField(blank=True)

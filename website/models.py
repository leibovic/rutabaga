from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

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

  # Rank used for sorting sisters by class year, then alphabetically
  def sort_rank(self):
    return "%s%s%s" % (self.class_year, self.user.last_name, self.user.first_name)
  sort_rank.short_decription = 'Sort Rank'

  def __unicode__(self):
    return unicode("%s %s" % (self.user.first_name, self.user.last_name))

class SisterForm(ModelForm):
  class Meta:
    model = Sister
    fields = ('phone_number', 'residence', 'hometown', 'bio', 'interests')

class Event(models.Model):
  name = models.CharField(max_length=100)
  date = models.DateField()
  points = models.IntegerField()

  # The sisters who were at the event
  sisters = models.ManyToManyField(Sister, blank=True)

  def __unicode__(self):
    return unicode("%s (%s)" % (self.name, self.date))

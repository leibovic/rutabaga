from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

class Residence(models.Model):
  name = models.CharField(max_length=100)

  def __unicode__(self):
    return unicode(self.name)

class Major(models.Model):
  number = models.CharField(max_length=10)
  description = models.CharField(max_length=100)

  def __unicode__(self):
    return unicode("%s - %s" % (self.number, self.description))

STATUS = (
  (0, 'Active'),
  (1, 'Alum'),
  (2, 'New Member'),
  (3, 'PRC')
)

class Sister(models.Model):
  user = models.ForeignKey(User, unique=True)
  class_year = models.IntegerField()
  status = models.IntegerField(choices=STATUS)
  photo_url = models.CharField(max_length=100, blank=True)

  residence = models.ForeignKey(Residence, null=True, blank=True)
  major = models.ForeignKey(Major, null=True, blank=True)
  majors = models.ManyToManyField(Major, null=True, blank=True, related_name='sister_majors')
  phone_number = models.CharField(max_length=10, blank=True)

  hometown = models.CharField(max_length=100, blank=True)
  bio = models.TextField(blank=True)
  interests = models.TextField(blank=True)

  big = models.ForeignKey('Sister', null=True, blank=True, related_name='sister_big')
  little = models.ForeignKey('Sister', null=True, blank=True, related_name='sister_little')
  littles = models.ManyToManyField('Sister', null=True, blank=True)

  memory = models.TextField(blank=True)
  why_axo = models.TextField(blank=True)
  what_axo_means = models.TextField(blank=True)
  

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
    fields = ('phone_number', 'residence', 'major', 'majors', 'hometown', 'bio', 'interests', 'big', 'little', 'littles', 'memory', 'why_axo', 'what_axo_means')

class Event(models.Model):
  name = models.CharField(max_length=100)
  date = models.DateField()
  points = models.IntegerField()

  # The sisters who were at the event
  sisters = models.ManyToManyField(Sister, blank=True)

  def __unicode__(self):
    return unicode("%s (%s)" % (self.name, self.date))

TERMS = (
  (0, 'Fall Election'),
  (1, 'Spring Election'),
  (2, 'Every Election')
)

TERM_LENGTH = (
  (1, 'One Semester'),
  (2, 'Two Semesters')
)

CLASSES = (
  (0, 'All Classes'),
  (1, 'Freshman'),
  (2, 'Sophomore'),
  (3, 'Junior'),
  (4, 'Senior')
)

class Office(models.Model):
  title = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  is_exec = models.BooleanField(default=False, verbose_name='Exec Position')
  is_committee = models.BooleanField(default=False, verbose_name='Committee Position')

  election_term = models.IntegerField(choices=TERMS, default=0)
  term_length = models.IntegerField(choices=TERM_LENGTH, default=1)
  # For positions that can only be held by a certain class year (e.g. CRSB Rep)
  class_year = models.IntegerField(choices=CLASSES, default=0, verbose_name='Eligible Class Year')

  current_officer = models.ForeignKey(Sister, blank=True, null=True)

  chain_of_command = models.IntegerField(default=0, blank=True, null=True)
  reports_to = models.ForeignKey('Office', default='EmptyOffice')

  def sort_rank(self):
    # Sort by reverse chain of command. Add title in case chain_of_command is accidentally tied.
    return "%s%s" % (100 - self.reports_to.chain_of_command, self.title)
  sort_rank.short_decription = 'Sort Rank'

  def __unicode__(self):
    return unicode(self.title)

EmptyOffice = Office(title="")

INTEREST_LEVELS = (
  (0, 'No'),
  (1, 'Yes'),
  (2, 'Maybe')
)

class OfficeInterest(models.Model):
  sister = models.ForeignKey(Sister)
  office = models.ForeignKey(Office)
  interest = models.IntegerField(choices=INTEREST_LEVELS, null=True)

  # Rank used for sorting results by office, then interest, then sister
  def sort_rank(self):
    return "%s%s%s" % (self.office, self.interest, self.sister.sort_rank())
  sort_rank.short_decription = 'Sort Rank'

  def __unicode__(self):
    return unicode("%s, %s" % (self.sister, self.office))

class Candidate(models.Model):
  # committee candidates can have more than one sister
  sisters = models.ManyToManyField(Sister)

  office = models.ForeignKey(Office)
  loi = models.TextField()

  def sort_rank(self):
    # Sort by reverse chain of command. Add title in case chain_of_command is accidentally tied.
    return "%s%s" % (100 - self.office.chain_of_command, self.office.title)
  sort_rank.short_decription = 'Sort Rank'

  def __unicode__(self):
    return unicode("%s, %s" % (self.sisters.all(), self.office))

class CandidateForm(ModelForm):
  class Meta:
    model = Candidate
    fields = ('sisters', 'office', 'loi')

class Vote(models.Model):
  office = models.ForeignKey(Office)
  candidate = models.ForeignKey(Candidate)

  # The sister casting this vote
  sister = models.ForeignKey(Sister)

  def __unicode__(self):
    return unicode("Vote for %s for %s" % (self.candidate, self.office))

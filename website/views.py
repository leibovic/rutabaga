from website.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import RequestContext
from django.conf import settings
from django.db.models import Count

def get_context(request):
  context = {}
  context['user'] = request.user
  if request.user.is_authenticated():
    try:
      context['sister'] = Sister.objects.get(user=request.user)
    except:
      pass
  return context

''' Page requests '''

def sisters(request):
  context = get_context(request)
  # Exclude alums and PRCs. Is there a way to get this from the STATUS data structure in models.py?
  context['sisters'] = Sister.objects.exclude(status=1).exclude(status=3)
  return render_to_response('sisters.html', context)

def sisters_profile(request, sister_id):
  context = get_context(request)
  context['profile_sister'] = Sister.objects.get(id=sister_id)
  return render_to_response('profile.html', context)

@login_required
def edit_profile(request):
  context = get_context(request)
  sister = context['sister']

  if request.method == 'POST':
    form = SisterForm(request.POST, instance=sister)
    if form.is_valid():
      form.save()
      context['success'] = True
  else:
    form = SisterForm(instance=sister)

  context['form'] = form
  return render_to_response("edit_profile.html", RequestContext(request, context))

''' Sisters only pages '''

@login_required
def sistersonly_directory(request):
  context = get_context(request)
  # Exclude alums
  context['sisters'] = Sister.objects.exclude(status=1)
  return render_to_response('sistersonly/directory.html', context)

@login_required
def sistersonly_events(request):
  context = get_context(request)
  context['events'] = Event.objects.all()
  return render_to_response('sistersonly/events.html', context)

@login_required
def sistersonly_events_attendance(request, event_id):
  context = get_context(request)
  event = Event.objects.get(id=event_id)
  sisters = Sister.objects.exclude(status=1)
  if request.method == 'POST':
    for sister in sisters:
      # The keys will be made up of sister ids
      if str(sister.id) in request.POST.keys():
        event.sisters.add(sister)
      else:
        # Call remove in case the sister was previously selected
        event.sisters.remove(sister)
    context['updated'] = True;

  context['event'] = event
  context['sisters'] = sisters
  return render_to_response('sistersonly/events_attendance.html', RequestContext(request, context))

@login_required
def sistersonly_feedback(request):
  context = get_context(request)
  if request.method == 'POST':
    message = request.POST['message']
    try:
      send_mail('Anonymous Sister Feedback', message, settings.DEFAULT_FROM_EMAIL,
                [settings.FEEDBACK_EMAIL], fail_silently=False)
      context['submitted'] = True
    except:
      context['error'] = True

  return render_to_response('sistersonly/feedback.html', RequestContext(request, context))

@login_required
def sistersonly_elections(request):
  context = get_context(request)
  return render_to_response('sistersonly/elections.html', context)

@login_required
def sistersonly_elections_ois(request):
  context = get_context(request)
  try:
    ois_open = settings.OIS_OPEN
  except:
    pass
  if not ois_open:
    context['ois_closed'] = True
    return render_to_response("sistersonly/elections_ois.html", RequestContext(request, context))

  #trying to filter out 
  #sister = context['sister']

  non_election_term = 1 - settings.ELECTION_TERM
  offices = Office.objects.filter(is_exec=settings.EXEC_ELECTION).exclude(election_term__exact=non_election_term)
  context['offices'] = offices

  if request.method == 'POST':
    sister = context['sister']
    results = []
    for office in offices:
      try:
        office_interest = OfficeInterest.objects.get(sister=sister, office=office)
      except:
        office_interest = OfficeInterest(sister=sister, office=office)
      try:
        office_interest.interest = request.POST[str(office.id)]
        office_interest.save()
      except:
        context['error'] = True
        return render_to_response("sistersonly/elections_ois.html", RequestContext(request, context))

    context['submitted'] = True

  return render_to_response("sistersonly/elections_ois.html", RequestContext(request, context))

@login_required
def sistersonly_elections_ois_results(request):
  context = get_context(request)
  non_election_term = 1 - settings.ELECTION_TERM
  context['results'] = OfficeInterest.objects.filter(office__is_exec=settings.EXEC_ELECTION).exclude(office__election_term=non_election_term)
  return render_to_response('sistersonly/elections_ois_results.html', context)

@login_required
def sistersonly_elections_loi(request):
  context = get_context(request)
  try:
    loi_open = settings.LOI_OPEN
  except:
    pass
  if not loi_open:
    context['loi_closed'] = True
    return render_to_response('sistersonly/elections_loi.html', RequestContext(request, context))

  if request.method == 'POST':
    form = CandidateForm(request.POST)
    if form.is_valid():
      try:
        # Delete any pre-existing LOIs
        candidate = Candidate.objects.get(sisters=form.cleaned_data['sisters'], office=form.cleaned_data['office'])
        candidate.delete()
      except:
        pass
      form.save()
      context['success'] = True
  else:
    form = CandidateForm()

  non_election_term = 1 - settings.ELECTION_TERM
  form.fields['office'].queryset = Office.objects.filter(is_exec=settings.EXEC_ELECTION).exclude(election_term=non_election_term).order_by('title')
  form.fields['sisters'].queryset = Sister.objects.exclude(status=1).order_by('user__last_name')
  context['form'] = form
  return render_to_response('sistersonly/elections_loi.html', RequestContext(request, context))

@login_required
def sistersonly_elections_loi_results(request):
  context = get_context(request)
  non_election_term = 1 - settings.ELECTION_TERM
  context['candidates'] = Candidate.objects.filter(office__is_exec=settings.EXEC_ELECTION).exclude(office__election_term=non_election_term)
  try:
    context['loi_results_open'] = settings.LOI_RESULTS_OPEN
  except:
    pass
  return render_to_response('sistersonly/elections_loi_results.html', context)

@login_required
def sistersonly_elections_slating(request):
  context = get_context(request)
  try: # Check to make sure slating is open
    slating_open = settings.SLATING_OPEN
  except:
    pass

  if not slating_open:
    context['slating_closed'] = True
    return render_to_response('sistersonly/elections_slating.html', RequestContext(request, context))

  # Check to make sure the user hasn't already voted
  voting_sister = context['sister']
  existing_votes = Vote.objects.filter(sister=voting_sister)
  if len(existing_votes) > 0:
    context['already_voted'] = True
    return render_to_response('sistersonly/elections_slating.html', RequestContext(request, context))

  if request.method == 'POST':
    non_election_term = 1 - settings.ELECTION_TERM
    offices = Office.objects.filter(is_exec=settings.EXEC_ELECTION).exclude(election_term=non_election_term)
    for office in offices:
      try: # Get the first candidate choice
        id1 = request.POST[str(office.id)+"-1"];
        candidate1 = Candidate.objects.get(id=id1)
        vote1 = Vote(office=office, candidate=candidate1, sister=voting_sister)
        vote1.save()
      except:
        pass

      try: # Get the second candidate choice
        id2 = request.POST[str(office.id)+"-2"]
        if id1 != id2:
          candidate2 = Candidate.objects.get(id=id2)
          vote2 = Vote(office=office, candidate=candidate2, sister=voting_sister)
          vote2.save()
      except:
        pass

    context['success'] = True
  else:
    non_election_term = 1 - settings.ELECTION_TERM
    context['candidates'] = Candidate.objects.filter(office__is_exec=settings.EXEC_ELECTION).exclude(office__election_term=non_election_term)

  return render_to_response('sistersonly/elections_slating.html', RequestContext(request, context))

@login_required
def sistersonly_elections_slating_results(request):
  context = get_context(request)
  # TODO: This should be done in the template, and with a more specific permission group
  context['can_view'] = request.user.is_staff

  results = []
  non_election_term = 1 - settings.ELECTION_TERM
  offices = Office.objects.filter(is_exec=settings.EXEC_ELECTION).exclude(election_term=non_election_term).order_by('title')
  for office in offices:
    # Count the number of votes for each candidate
    # Example: votes = [{'candidate__count': 2, 'candidate': 1}, ... ]
    votes = Vote.objects.filter(office=office).values('candidate').order_by().annotate(Count('candidate'))
    for vote in votes:
      vote['candidate'] = Candidate.objects.get(id=vote['candidate'])
    results.append({ 'office': office, 'votes': votes })
  context['results'] = results

  slating_sisters = []
  voter_aggregate = Vote.objects.values('sister').order_by().annotate()
  for item in voter_aggregate:
    slating_sisters.append(Sister.objects.get(id=item['sister']))
  context['slating_sisters'] = slating_sisters
  
  return render_to_response('sistersonly/elections_slating_results.html', context)

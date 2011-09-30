from website.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import RequestContext
from django.conf import settings

def secure_required(view_func):
    """Decorator makes sure URL is accessed over https."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.is_secure():
            if getattr(settings, 'HTTPS_SUPPORT', True):
                request_url = request.build_absolute_uri(request.get_full_path())
                secure_url = request_url.replace('http://', 'https://')
                return HttpResponseRedirect(secure_url)
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

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

@secure_required
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

@secure_required
@login_required
def sistersonly_elections_ois(request):
  context = get_context(request)
  offices = Office.objects.filter(is_exec=True)

  if request.method == 'POST':
    sister = context['sister']
    results = []
    for office in offices:
      try:
        office_interest = OfficeInterest.objects.get(sister=sister, office=office)
      except:
        office_interest = OfficeInterest(sister=sister, office=office)
      office_interest.interest = request.POST[str(office.id)]
      office_interest.save()
    context['submitted'] = True
  else:
    context['offices'] = offices

  return render_to_response("sistersonly/elections_ois.html", RequestContext(request, context))

@secure_required
@login_required
def sistersonly_elections_ois_results(request):
  context = get_context(request)
  context['results'] = OfficeInterest.objects.all()
  return render_to_response('sistersonly/elections_ois_results.html', context)

@secure_required
@login_required
def sistersonly_elections_loi(request):
  context = get_context(request)
  return render_to_response('sistersonly/elections_loi.html', context)

@secure_required
@login_required
def sistersonly_elections_slating(request):
  context = get_context(request)
  return render_to_response('sistersonly/elections_slating.html', context)


from website.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import RequestContext

def get_context(request):
  context = {}
  if request.user.is_authenticated():
    try:
      context['sister'] = Sister.objects.get(user=request.user)
    except:
      pass
  context['current_page'] = request.path.replace('/', '')
  return context

''' Page requests '''

def sisters(request):
  context = get_context(request)
  # Exclude alums and PRCs. Is there a way to get this from the STATUS data structure in models.py?
  context['sisters'] = Sister.objects.exclude(status=1).exclude(status=3)
  return render_to_response('sisters.html', context)

def contact(request):
  context = get_context(request)
  return render_to_response('contact.html', context)


''' Sisters only pages '''

@login_required
def sistersonly(request):
  context = get_context(request)
  return render_to_response('sistersonly/index.html', context)

@login_required
def sistersonly_profile(request, sister_id):
  context = get_context(request)
  context['profile_sister'] = Sister.objects.get(id=sister_id)
  return render_to_response('sistersonly/profile.html', context)

@login_required
def sistersonly_directory(request):
  context = get_context(request)
  # Exclude alums
  context['sisters'] = Sister.objects.exclude(status=1)
  return render_to_response('sistersonly/directory.html', context)

@login_required
def sistersonly_officers(request):
  context = get_context(request)
  return render_to_response('sistersonly/officers.html', context)

@login_required
def sistersonly_house(request):
  context = get_context(request)
  return render_to_response('sistersonly/house.html', context)

@login_required
def sistersonly_elections(request):
  context = get_context(request)
  return render_to_response('sistersonly/elections.html', context)

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
      send_mail('Anonymous Sister Feedback', message, 'axothetaomicron@gmail.com',
                ['margaret.leibovic@gmail.com'], fail_silently=False)
      context['submitted'] = True
    except:
      context['error'] = True

  return render_to_response('sistersonly/feedback.html', RequestContext(request, context))


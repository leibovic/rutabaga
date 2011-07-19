from website.models import *
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def get_user(request):
  if request.user.is_authenticated():
    return request.user
  return None

''' Page requests '''

def index(request):
  return render_to_response('index.html', {'user': get_user(request)})

def about(request):
  return render_to_response('about.html', {'user': get_user(request)})

def sisters(request):
  # Exclude alums and PRCs. Is there a way to get this from the STATUS data structure in models.py?
  sisters = Sister.objects.exclude(status=1).exclude(status=3)
  return render_to_response('sisters.html', {'user': get_user(request), 'sisters': sisters})

def philanthropy(request):
  return render_to_response('philanthropy.html', {'user': get_user(request)})

def social(request):
  return render_to_response('social.html', {'user': get_user(request)})

def recruitment(request):
  return render_to_response('recruitment.html', {'user': get_user(request)})

def parents(request):
  return render_to_response('parents.html', {'user': get_user(request)})

def alumnae(request):
  return render_to_response('alumnae.html', {'user': get_user(request)})

def contact(request):
  return render_to_response('contact.html', {'user': get_user(request)})

''' Sisters only pages '''

@login_required(login_url='/accounts/login/')
def sistersonly(request):
  return render_to_response('sistersonly.html', {'user': get_user(request)})

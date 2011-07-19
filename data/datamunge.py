#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
datamunge.py
Creates users, sisters, and residences from sisters.csv and residences.csv files.
'''

import csv
import re
from django.contrib.auth.models import User
from website.models import Sister, Residence

def add_residences():
  reader = csv.reader(open('residences.csv', 'rb'), delimiter=';')
  for row in reader:
    residence = Residence(name=unicode(row[0], "utf-8"))
    residence.save()
    print 'added residence to database:', residence

class Data:
  ID=0
  FIRST_NAME=1
  LAST_NAME=2
  CLASS_YEAR=3
  RESIDENCE=5
  USERNAME=6
  PHONE_NUMBER=7
  STATUS=8
  HOMETOWN=10
  PHOTO_URL=11
  INTERESTS=14
  BIO=18

def add_sisters():
  reader = csv.reader(open('sisters.csv', 'rb'), delimiter=';')
  for row in reader:
    try:
      user = User.objects.get(username=row[Data.USERNAME])
      print 'got user from database:', user
    except:
      user = User(username=row[Data.USERNAME],
                  email=row[Data.USERNAME]+'@mit.edu',
                  first_name=row[Data.FIRST_NAME],
                  last_name=row[Data.LAST_NAME])
      user.save()
      print 'added user to database:', user

    # assume only Active or Alum sisters
    status = 0 if row[Data.STATUS] == 'Active' else 1

    # clean up phone numbers and get rid of invalid phone numbers
    raw_phone_number = re.sub(r'\D', '', row[Data.PHONE_NUMBER])
    phone_number = raw_phone_number if len(raw_phone_number) == 10 else ''

    hometown = row[Data.HOMETOWN]
    if hometown == 'NULL' or hometown == '0': hometown = ''

    interests = row[Data.INTERESTS]
    if interests == 'NULL' or interests == '0': interests = ''

    bio = row[Data.BIO]
    if bio == 'NULL' or bio == '0': bio = ''  

    sister = Sister(user=user,
                    class_year=row[Data.CLASS_YEAR],
                    status=status,
                    phone_number=phone_number,
                    hometown=hometown,
                    photo_url=row[Data.PHOTO_URL],
                    interests=interests,
                    bio=bio)

    residence_name = row[Data.RESIDENCE]
    try:
      sister.residence = Residence.objects.get(name=residence_name)
    except:
      print sister, 'has an invalid residence:', residence_name

    sister.save()
    print 'added sister to database:', sister

#add_residences()
add_sisters()

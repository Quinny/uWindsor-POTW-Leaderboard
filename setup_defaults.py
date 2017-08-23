import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "potwleaderboard.settings")

import django
django.setup()

from problem.models import Problem
from django.contrib.auth.models import User

print "Creating default problem"
p = Problem.objects.create(year=3005, week=1, description="dummy text",
                           nicename="First Problem", published=True)
p.save()

print "Creating admin account"
admin_user = raw_input("enter the admin's username: ")
password = raw_input("enter the admin's password: ")
admin = User.objects.create_user(admin_user, admin_user, password)
admin.save()

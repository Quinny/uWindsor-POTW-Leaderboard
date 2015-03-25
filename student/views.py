from django.shortcuts import render, redirect
from student.models import Student
from django.db.models import Count
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import errorpage
import hashlib
import hmac
import datetime
import re

def index(request):
    # Maybe do this in the database?
    top_users = sorted(Student.objects.all(), key=lambda s: s.solution_count, reverse=True)
    return render(request, "student/index.html",
        {"students" : top_users })

def profile(request, uid):
    try:
        s = Student.objects.get(student_id=uid)
    except:
        return errorpage.views.index(request)
    return render(request, "student/student.html",
            {"student" : s,
             "email_md5" : hashlib.md5(s.student_id + "@uwindsor.ca").hexdigest(),
             "solutions" : s.solution_set.order_by("week")
            }
        )

def sign_up(request, error=None, success=None):
    return render(request, "student/signup.html",
            {"error" : error,
             "success" : success
            }
        )

def send_verify(request):
    if 'uwinid' not in request.POST or len(request.POST['uwinid']) == 0:
        return sign_up(request, "Please enter your uWindsor ID", {})
    uwinid_check = re.compile("(\d|[a-zA-Z])+$")
    if uwinid_check.match(request.POST['uwinid']) == None:
        return sign_up(request, "That uWindsor ID is invalid", {})
    try:
        u = Student.objects.get(student_id=request.POST['uwinid'])
        if u is not None:
            return sign_up(request, "That uWindsor ID is already registered", {})
    except:
        pass
    now = datetime.datetime.now()
    verify_hash = hmac.new(settings.EMAIL_SECRET,
            request.POST['uwinid'] + str(now.hour)).hexdigest()
    send_mail("uWindsor POTW - Confirm ID",
            "Click the following link to confirm your uWindsor ID and begin"+\
            " submitting your problem of the week solutions.\n"+\
            settings.SITE_URL+"/student/verify/" + request.POST['uwinid'] + "/"+\
            verify_hash,
            "noreply@potw.quinnftw.com",
            [request.POST['uwinid'] + "@uwindsor.ca"],
            fail_silently=False)
    return sign_up(request, None, "Email Sent")

def verify(request, uwinid, verify_hash):
    try:
        # Because at this point they are just spam refreshing the page
        u = Student.objects.get(student_id=uwinid)
        if u is not None:
            return redirect("/")
    except:
        pass
    now = datetime.datetime.now()
    check = hmac.new(settings.EMAIL_SECRET,
            uwinid + str(now.hour)).hexdigest()
    if hmac.compare_digest(str(check), str(verify_hash)):
        s_code = get_random_string(length=10)
        Student.objects.create(student_id = uwinid,
                submit_code = s_code)
        send_mail("uWindsor POTW - Submission Code",
                "Your submission code is " + s_code + ", keep it safe.",
                "noreply@potw.quinnftw.com",
                [uwinid + "@uwindsor.ca"],
                fail_silently=False)
        return render(request, "student/verify_success.html", {"code" : s_code})
    else:
        return render(request, "student/verify_success.html",
                {"error" : "This link is either expiried or invalid"})

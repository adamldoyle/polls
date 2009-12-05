from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from polls.models import *

@login_required
def poll_vote(request):
    if request.user.is_authenticated() and request.POST.has_key('poll_choice'):
        c_id = request.POST['poll_choice']
        c = get_object_or_404(Choice, pk=c_id)
        v = Vote(choice=c, poll=c.poll, user=request.user)
        if c.other_field:
            v.other = request.POST['other_choice_%s' % c_id]
        v.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
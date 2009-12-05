from django.db import models
from django.contrib import admin
from mixins.models import DateMixin, UserMixin

class Poll(DateMixin, UserMixin):
    question = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    other_field = models.BooleanField(default=False)

    def __unicode__(self):
        return self.choice
    
    def vote_count(self):
        return self.vote_set.all().count()
    
    def vote_percentage(self):
        try:
            return int((float(self.vote_count()) / self.poll.vote_set.all().count()) * 100)
        except ZeroDivisionError:
            return 0
    
class Vote(DateMixin, UserMixin):
    choice = models.ForeignKey(Choice)
    poll = models.ForeignKey(Poll)
    other = models.CharField(max_length=200, null=True, blank=True)
    
    def __unicode__(self):
        if self.choice.other_field:
            return u"%s chose %s (%s)." % (self.user, self.choice, self.other)
        else:
            return u"%s chose %s." % (self.user, self.choice)

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote)
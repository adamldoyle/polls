from django import template
from mixins.helpers import VariableNode, VariableTag
from polls.models import Poll

register = template.Library()

class PollNode(VariableNode):
    def setVariable(self, context):
        try:
            poll = Poll.objects.all().newest(1)[0]
            request = context['request']
            if request.user.is_authenticated() and len(poll.vote_set.filter(user=request.user)) > 0:
                poll.voted = True
        except IndexError:
            poll = None
        except KeyError:
            poll = None
        return poll

def current_poll(parser, token):
    return VariableTag(parser, token, PollNode)
register.tag('current_poll', current_poll)
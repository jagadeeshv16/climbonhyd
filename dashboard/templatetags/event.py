from django import template
from dashboard.models import SiteContent

register = template.Library()

@register.simple_tag
def site_names():
	events = SiteContent.objects.filter(active=True).order_by('index')
	return events

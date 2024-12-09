from django import template

register = template.Library()


@register.filter
def is_moderator(user):
    return user.groups.filter(name__in=["Moderator"]).exists()


@register.filter
def is_receptionist(user):
    return user.groups.filter(name__in=["Receptionist"]).exists()
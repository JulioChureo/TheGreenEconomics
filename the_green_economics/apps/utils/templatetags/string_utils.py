from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def find_word(context, word):
    """
    Find a specific word in the current request's GET parameters.
    """
    d = context["request"].GET.copy()
    return word in d.values()

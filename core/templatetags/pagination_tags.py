from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def query_transform(context, page):

    request = context["request"]
    params = request.GET.copy()
    params["page"] = page

    return params.urlencode()

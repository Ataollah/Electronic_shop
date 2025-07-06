from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def update_page(context, page_num):
    request = context['request']
    params = request.GET.copy()
    params['page'] = page_num
    return params.urlencode()
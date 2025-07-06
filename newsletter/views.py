from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class SubscribeSuccessView(TemplateView):
    template_name = 'newsletter/Success/subscribe_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

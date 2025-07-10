from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from blog.models import Post
from newsletter.forms import SubscriberForm


class PermissionDeniedView(View):
    def get(self, request, exception):
        return render(request, '403.html', status=403)


class PageNotFoundView(View):
    def get(self, request, exception):
        return render(request, '404.html', status=404)


class HomeView(TemplateView):
    template_name = 'Pages/Home/home.html'

    def get(self, request, *args, **kwargs):
        form = SubscriberForm()
        return render(request, self.template_name, {'sub_form': form})

    def post(self, request, *args, **kwargs):
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('newsletter:success')
        print('sub form error', form.non_field_errors())
        return render(request, self.template_name, {'sub_form': form})

from django.shortcuts import render, redirect
from django.template.defaultfilters import title
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from newsletter.forms import SubscriberForm
from blog.models import Post
from siteInfo.cache.site_info_cache import getSiteInfo
from siteInfo.froms import ContactUSForm
from siteInfo.models import FAQ


# Create your views here.
class BaseCommonPageView(TemplateView):
    template_name = 'Pages/Common/common.html'
    page_type = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = Post.objects.filter(page_type=self.page_type,is_published=True).first()
        context['post'] = post
        return context

class AboutUsView(BaseCommonPageView):
   # template_name = 'Page/AboutUS/about_us.html'
    page_type = 'about_us'

class PrivacyPolicyView(BaseCommonPageView):
   # template_name = 'Page/PrivacyPolicy/privacy_policy.html'
    page_type = 'privacy_policy'

class TermsOfUseView(BaseCommonPageView):
   # template_name = 'Page/TermsOfUse/terms_of_use.html'
    page_type = 'terms_of_use'


class FAQView(TemplateView):
    template_name = 'Pages/FAQ/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs = FAQ.objects.all()
        context['faqs'] = faqs
        return context


class ContactUsView(View):
    template_name = 'Pages/ContactUS/contact_us.html'

    def get(self, request):
        site_info = getSiteInfo()
        form = ContactUSForm()
        context = {'siteInfo': site_info,  'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        site_info = getSiteInfo()
        form = ContactUSForm(request.POST or None)

        if form.is_valid():
            form.save()
            request.session['title'] = "ارسال پیام"
            request.session['message'] = "پیام شما با موفقیت ارسال شد"
            return redirect('message-view')
        else:
            print(form.errors)

        return render(request, self.template_name, {'siteInfo': site_info, 'form': form})



class MessagesView(TemplateView):
    template_name = 'Pages/Message/message.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        message = self.request.session.pop('message', None)
        title = self.request.session.pop('title', None)
        context['title'] = title
        context['message'] = message
        return context



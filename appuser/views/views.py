from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from appuser.forms import  CreateUserForm, CustomAuthenticationForm, CustomSetPasswordForm, \
    CandidPhoneVerificationForm, VerifyCodeForm , UserPhoneVerificationForm
from appuser.models import  AppUser
from Utility.VerificationMessageSender import VerificationMessageSender
from iran.models import Province



class LoginView(View):
    template_name = 'appuser/Login/login.html'

    def get(self, request):
        form = CustomAuthenticationForm()
        context = {'form':form}
        return render(request, self.template_name,context)

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            print('user in login : ',user)
            # user = form.get_user()
            next_url = request.GET.get('next', '/')
            if user is not None:
                login(request, user)
                if not form.cleaned_data.get('remember_me'):
                    print('Remember me is checked')
                    request.session.set_expiry(0)  # Session will expire when the user closes the browser
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                print('Session expiry age:', request.session.get_expiry_age())
                return redirect(next_url)
        context = {'form': form}
        return render(request, self.template_name, context)

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login-view')



class BasePhoneVerificationView(View):
    form_class = None
    template_name = None

    def get(self, request):
        form = self.form_class()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form, request)
        return self.form_invalid(form, request)

    def form_valid(self, form, request):
        raise NotImplementedError("Subclasses must implement `form_valid` method.")

    def form_invalid(self, form, request):
        context = {'form': form}
        return render(request, self.template_name, context)

class CandidPhoneVerificationView(BasePhoneVerificationView):
    form_class = CandidPhoneVerificationForm
    template_name = 'appuser/PhoneVerification/phone_verification.html'

    def form_valid(self, form, request):
        username = form.cleaned_data.get("username")
        sender = VerificationMessageSender(username)
        sender.sendCode()
        request.session['candid_username'] = username
        return redirect('verify-candid-code-view')

class UserPhoneVerificationView(BasePhoneVerificationView):
    form_class = UserPhoneVerificationForm
    template_name = 'appuser/PhoneVerification/phone_verification.html'

    def form_valid(self, form, request):
        username = form.cleaned_data.get("username")
        sender = VerificationMessageSender(username)
        sender.sendCode()
        request.session['username'] = username
        print('username in session:', request.session['username'])
        return redirect('verify-user-code-view')

class BaseVerifyCodeView(View):
    template_name = None
    session_key = None
    redirect_url = None

    def get(self, request):
        username = request.session.get(self.session_key)
        print('username in verify :', username)
        if not username:
            return redirect('home')
        form = VerifyCodeForm(username=username)
        context = {'form': form, 'username': username}
        return render(request, self.template_name, context)

    def post(self, request):
        username = request.session.get(self.session_key)
        form = VerifyCodeForm(request.POST, username=username)
        print(username)
        if form.is_valid():
            return redirect(self.redirect_url)
        context = {'form': form, 'username': username}
        return render(request, self.template_name, context)

class VerifyCandidCodeView(BaseVerifyCodeView):
    template_name = 'appuser/VerifyCode/verify_code.html'
    session_key = 'candid_username'
    redirect_url = 'create-user-view'


class VerifyUserCodeView(BaseVerifyCodeView):
    template_name = 'appuser/VerifyCode/verify_code.html'
    session_key = 'username'
    redirect_url = 'reset-password-view'


class CreateUserView(View):
    template_name = 'appuser/CreateUser/create_user.html'

    def get(self, request):
        if request.session.get('candid_username') is None:
            return redirect('home')

        form = CreateUserForm(initial={'username': request.session.get('candid_username')})
        provinces = Province.objects.all()
        context = {'form':form, 'provinces': provinces}
        return render(request, self.template_name, context)

    def post(self,request):
        username = request.session.get('candid_username')
        if username is None:
            return redirect('home')
        form = CreateUserForm(request.POST, request.FILES, initial={'username':username})
        provinces = Province.objects.all()
        if form.is_valid():
            form.save()
            addToCustomerGroup(username)
            return redirect('create-user-succeeded-view')
        else:
            print("errors : ",form.errors)
        context = {'form': form,'provinces': provinces}
        return render(request, self.template_name, context)


def addToCustomerGroup(username):
    user = AppUser.objects.filter(username=username).first()
    user_group, created = Group.objects.get_or_create(name='Customer')
    user.groups.add(user_group)
    user.save()

class CreatedUserSucceededView(View):
    template_name = 'appuser/CreateUserSucceeded/create_user_succeeded.html'
    def get(self, request):
        # if request.session.get('candid_username') is None:
        #     return redirect('home')
        request.session['candid_username'] = None
        request.session.save()

        return render(request, self.template_name)



class ResetPasswordView(View):
    template_name = 'appuser/ResetPassword/reset-password.html'
    def get(self, request):
        user = AppUser.objects.filter(username=request.session.get('username')).first()
        if user is None:
            return redirect('user-phone-verification-view')

        form = CustomSetPasswordForm(user)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request):
        user = AppUser.objects.filter(username=request.session.get('username')).first()
        if user is None:
            return redirect('user-phone-verification-view')

        form = CustomSetPasswordForm(user,request.POST)
        if form.is_valid():
            form.save()
            return redirect('reset-password-done-view')
        context = {'form': form}
        return render(request, self.template_name, context)


class ResetPasswordDoneView(TemplateView):
    template_name = 'appuser/ResetPassword/reset-pass-done.html'

    def get(self, request, *args, **kwargs):
        request.session['username'] = None
        return super().get(request, *args, **kwargs)

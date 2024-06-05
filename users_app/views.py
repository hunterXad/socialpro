from django.shortcuts import render, redirect , get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm , LoginForm , ProfileUpdateForm
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.models import User



    

# Create your views here.


from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
      
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
       
        return self.get(request, *args, **kwargs)


class UserSignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('home')  

    def form_valid(self, form):
        
        form.save()

       
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']  
        user = authenticate(username=username, password=password)
        if user:
            login(self.request, user)
        
        return super().form_valid(form)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
        
class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

    def post(self, request, *args, **kwargs):
        
        return self.get(request, *args, **kwargs)
   


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileUpdateForm()
        return render(request, 'profile.html', {'form': form})

    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
           
            return render(request, 'profile.html', {'form': form})


class ProfileDetailView(DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        return User.objects.get(username=username)

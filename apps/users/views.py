from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .models import User, UserAddress
from .forms import UserRegistrationForm, UserLoginForm, UserAddressForm

@login_required
def add_address(request):
    """
    Add a new delivery address for the user.
    """
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address added successfully!')
            
            # Redirect to checkout if they came from there
            next_url = request.GET.get('next', 'users:profile')
            return redirect(next_url)
    else:
        form = UserAddressForm()
        
    context = {
        'form': form,
    }
    return render(request, 'pages/users/add_address.html', context)


class LoginView(FormView):
    """
    Custom login view for email-based authentication.
    """
    template_name = 'pages/users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('products:home')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f'Welcome back, {user.get_display_name()}!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid email or password.')
            return self.form_invalid(form)


class RegisterView(CreateView):
    """
    User registration view.
    """
    model = User
    form_class = UserRegistrationForm
    template_name = 'pages/users/register.html'
    success_url = reverse_lazy('users:login')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('products:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, 'Account created successfully! Please log in.')
        return super().form_valid(form)


@login_required
def logout_view(request):
    """
    Logout view.
    """
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('products:home')


@login_required
def profile_view(request):
    """
    User profile view.
    """
    context = {
        'user': request.user,
    }
    return render(request, 'pages/users/profile.html', context)
from django.shortcuts import render
from django.contrib.auth import login
from .forms import CustomUserForm
from .utils import generate_phrase, send_email


def sign_up(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.recovery_phrase = generate_phrase()
            user.save()
            login(request, user)
            send_email(user)
            pass
    else:
        form = CustomUserForm()
    return render(request, 'accounts/signup.html')
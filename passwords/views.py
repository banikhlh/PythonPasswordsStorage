from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PasswordEntryForm
from .models import PasswordEntry
from .utils import generate_password


@login_required
def password_list(request):
    passwords = PasswordEntry.objects.filter(user=request.user)
    return render(request, "passwords/password_list.html", {"passwords": passwords})


@login_required
def add_password(request):
    if request.method == "POST":
        form = PasswordEntryForm(request.POST)
        if form.is_valid():
            password_entry = form.save(commit=False)
            password_entry.user = request.user
            password_entry.save()
            messages.success(request, "Password successfully added")
            return redirect("password_list")
    else:
        form = PasswordEntryForm()

    return render(request, "passwords/password_form.html", {"form": form})


@login_required
def generate_password_view(request):
    password = generate_password()
    return render(
        request, "passwords/generate_password.html", {"generated_password": password}
    )

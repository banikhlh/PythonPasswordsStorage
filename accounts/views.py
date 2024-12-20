from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render

from .forms import CustomUserForm, RecoveryPhraseForm
from .models import CustomUser
from .utils import generate_phrase, send_email, send_phrase_email


def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])
            user.phrase = generate_phrase()
            user.save()
            login(request, user)
            send_email(user)
            redirect("accounts/phrase")
    else:
        form = CustomUserForm()
    return render(request, "accounts/signup.html", {"form": form})


def phrase(request):
    if not request.user.is_authenticated:
        return redirect("accounts/signin")
    phrase = request.user.phrase
    context = {
        "phrase": phrase,
        "phrase_list": phrase.split(" "),
    }
    send_phrase_email(request.user)
    return render(request, "accounts/phrase.html", context)


@login_required
def verify_email(request):
    user = request.user
    if user.verified:
        messages.info(request, "Your email is already verified.")
        return redirect("accounts/home")
    if request.method == "POST":
        code = request.POST.get("code")
        if code == user.code:
            user.verified = True
            user.code = None
            user.save()
            messages.success(request, "Your email has been verified.")
            return redirect("accounts/phrase")
        else:
            messages.error(request, "Invalid verification code.")
    return render(request, "accounts/verify_email.html")


@login_required
def reverify_email(request):
    user = request.user
    if user.verified:
        messages.info(request, "Your email is already verified.")
        return redirect("accounts/home")
    send_email(user)
    messages.success(request, "A new verification email has been sent.")
    return redirect("accounts/verify_email")


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "accounts/signin.html", {"form": form})


def signout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("accounts:signin")


def recovery_signin(request):
    if request.method == "POST":
        form = RecoveryPhraseForm(request.POST)
        if form.is_valid():
            recovery_phrase = form.cleaned_data["words"]
            try:
                user = CustomUser.objects.get(recovery_phrase=recovery_phrase)
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect("accounts:dashboard")
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid recovery phrase.")
    else:
        form = RecoveryPhraseForm()
    return render(request, "accounts/recovery.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "accounts/dashboard.html")

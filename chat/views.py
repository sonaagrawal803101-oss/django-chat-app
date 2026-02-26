from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def home(request):
    if request.method == "POST":
        content = request.POST.get("message")
        Message.objects.create(user=request.user, content=content)
        return redirect("home")

    messages = Message.objects.all().order_by("timestamp")
    return render(request, "chat.html", {"messages": messages})
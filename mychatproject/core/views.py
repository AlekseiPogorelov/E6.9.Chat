from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import ChatRoom
from chat.forms import SignUpForm, ProfileForm, UserForm
from django.shortcuts import get_object_or_404

def home(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    chatrooms = ChatRoom.objects.filter(participants=request.user) \
        if request.user.is_authenticated \
        else []
    users = User.objects.exclude(id=request.user.id) \
        if request.user.is_authenticated \
        else []

    context = {
        'form': form,
        'chatrooms': chatrooms,
        'users': users,
    }
    return render(request, 'core/home.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('home')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'core/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def private_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chatroom = ChatRoom.objects.filter(participants=request.user).filter(participants=other_user).first()
    if not chatroom:
        chatroom = ChatRoom.objects.create(
            name=f"Chat {request.user.username} & {other_user.username}",
            owner=request.user
        )
        chatroom.participants.add(request.user, other_user)
    return redirect('chat_room', room_id=chatroom.id)
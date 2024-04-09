from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import messages
from .forms import UserForm, ProfileForm
from .models import *
import json



@login_required(login_url='singin')
def chats(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    friend_messages = []
    num_of_msg = 0
    for friend in friends:
        last_message = ChatMessage.objects.filter(sender__in=[request.user, friend], receiver__in=[request.user, friend]).last()
        num_of_msg += ChatMessage.objects.filter(sender=friend, receiver=request.user, seen=False).count()
        friend_messages.append({
            "friend": friend,
            "last_message": last_message,
            "num_msg": num_of_msg
        })
    num_notification = Notification.objects.filter(
        receiver=request.user, seen=False).count()
    num_friend_request = FriendRequest.objects.filter(
        receiver=request.user, seen=False).count()
    context = {"profile": profile, "num_notif": num_notification, "num_friend_req": num_friend_request, "friends": friends, "friend_messages": friend_messages, "num_msg": num_of_msg}
    print(friends)
    return render(request, "mychathtml/index.html", context)

@login_required(login_url='singin')
def clear_chat(request, pk):
    if request.method == 'POST':
        user = request.user
        friend = get_object_or_404(get_user_model(), pk=pk)
        ChatMessage.objects.filter(sender=user, receiver=friend).delete()
        ChatMessage.objects.filter(sender=friend, receiver=user).delete()

        return redirect("chats")
    else:
        return HttpResponseBadRequest('Invalid request method.')

@login_required(login_url='singin')
def detail(request, pk):
    users = get_user_model()
    user = users.objects.get(id=pk)
    main_user = [request.user, user]
    profile = Profile.objects.get(user=user)
    chats = ChatMessage.objects.filter(sender__in=main_user, receiver__in=main_user)
    chats.update(seen=True)
    context = {"profile": profile, "chats": chats}

    return render(request, "mychathtml/detail.html", context)

@login_required(login_url='login')
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user)
    notifications.update(seen=True)
    num_not = notifications.count()
    context = {"notifications": notifications, "num_not": num_not}
    return render(request, "mychathtml/notification.html", context)


def register(request):
    if request.user.is_authenticated:
        return redirect("chats")
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("chats")
        else:
            print(form.errors)
    context = {"form": form}
    return render(request, "mychathtml/register.html", context)


def singin(request):
    if request.user.is_authenticated:
        return redirect("chats")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("chats")

        else:
            messages.warning(request, "Invalid credentials")
    return render(request, "mychathtml/singin.html")


def signout(request):
    logout(request)
    return redirect("singin")


def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("chats")
    context = {"form": form}
    return render(request, "mychathtml/update_profile.html", context)


def friend_request(request):
    user = request.user
    friend_requests = FriendRequest.objects.filter(receiver=user)
    num_friend_requests = friend_requests.count()
    context = {"f_requests": friend_requests, "num_friend_requests": num_friend_requests}
    return render(request, "mychathtml/friend_request.html", context)


def suggestion(request):
    all_user = get_user_model()
    user = request.user
    users = all_user.objects.all()
    profiles = Profile.objects.all()
    profile = Profile.objects.get(user=user)
    profile_friends = profile.friends.all()
    friends_count_list = [(profile.user_id, profile.friends.count()) for profile in profiles]
    print(friends_count_list)
    suggested_friends = all_user.objects.exclude(profile__friends__in=profile_friends).exclude(profiles=profile)
    friend_request = FriendRequest.objects.filter(receiver__in=suggested_friends, sender=request.user)
    num_friend_suggestions = suggested_friends.count()

    context = {"s_friends": suggested_friends, "f_requests": friend_request, "num_friend_suggestions": num_friend_suggestions, "friends_count_list": friends_count_list}
    return render(request, "mychathtml/suggestions.html", context)


def send_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    receiver = user.objects.get(id=user_id)
    friend_request = FriendRequest.objects.create(sender=request.user, receiver=receiver)
    return JsonResponse("it is going", safe=False)


def cancel_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    receiver = user.objects.get(id=user_id)
    friend_request = FriendRequest.objects.get(sender=request.user, receiver=receiver)
    friend_request.delete()
    return JsonResponse("it is giving", safe=False)


def accept_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    n_user = user.objects.get(id=user_id)
    profile = Profile.objects.get(user_id=request.user.id)
    profile2 = Profile.objects.get(user_id=user_id)
    f_request = FriendRequest.objects.get(sender=n_user, receiver=request.user)
    msg = None
    notification = None
    print(f_request)
    if profile:
        if profile.friends.filter(id=user_id).exists():
            profile.friends.remove(n_user)
            msg = "no"
        else:
            profile.friends.add(n_user)
            f_request.delete()
            notification = Notification.objects.create(sender=request.user, receiver=n_user, description=f"Hi, {request.user.username} accepted your friend request.")
            msg = "yes"
    if profile2:
        if profile2.friends.filter(id=request.user.id).exists():
            profile2.friends.remove(request.user)
        else:
            profile2.friends.add(request.user)

    return JsonResponse(msg, safe=False)


def reject_friend_request(request):
    data = json.loads(request.body)
    user_id = data["id"]
    user = get_user_model()
    n_user = user.objects.get(id=user_id)
    f_request = FriendRequest.objects.get(sender=n_user, receiver=request.user)
    f_request.delete()
    return JsonResponse("it is giving", safe=False)


def fetch_friend_request(request):
    num_friend_request = FriendRequest.objects.filter(receiver=request.user, seen=False).count()
    return JsonResponse(num_friend_request, safe=False)


def fetch_notification(request):
    num_of_notification = Notification.objects.filter(receiver=request.user, seen=False).count()
    return JsonResponse(num_of_notification, safe=False)


def createChat(request):
    data = json.loads(request.body)
    sender = request.user.id
    receiver = data["receiver_id"]
    msg = data["msg"]
    chat = ChatMessage.objects.create(sender_id=sender, receiver_id=receiver, message=msg, seen=False)
    try:
        chat = ChatMessage.objects.filter(sender_id=receiver, receiver_id=sender, seen=False)
        num_chat = chat.last().id
    except:
        num_chat = 0
    return JsonResponse(num_chat, safe=False)


def getChats(request):
    data = json.loads(request.body)
    sender = data["sender_id"]
    print(sender)
    try:
        chat = ChatMessage.objects.filter(sender_id=sender, receiver_id=request.user.id, seen=False)
        new_msg = chat.last().message
        msg_id = chat.last().id
    except:
        new_msg = "no chat"
        msg_id = 0
    chat_info = {"id": msg_id, "msg": new_msg}
    return JsonResponse(chat_info, safe=False)

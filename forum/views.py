from django.shortcuts import render
from forum.models import Comment
from django.http import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
User = get_user_model()

def show_forum(request):
    '''
    Show forum tanpa login
    '''
    return render(request, "main_page_forum.html")

def show_forum_json(request):
    threads = Comment.objects.filter(is_thread=True).order_by('-replies', 'date')
    return HttpResponse(serializers.serialize("json", threads), content_type="application/json")

def get_user_json(request, id):
    user = User.objects.filter(pk=id)
    json_data = json.loads(serializers.serialize("json", user))
    logged_in = User.objects.filter(pk=request.user.pk)

    if (len(logged_in) < 1):
        json_data[0]["can_delete"] = False
    elif (logged_in.values('is_staff')[0]['is_staff'] == True) or (json_data[0]['pk'] == request.user.pk):
        json_data[0]["can_delete"] = True
    else:
        json_data[0]["can_delete"] = False
    return HttpResponse(json.dumps(json_data), content_type="application/json")

def detailed_forum(request, id):
    '''
    Show detail dari forum thread
    '''
    return render(request, "detailed_page_forum.html")

def detailed_forum_json(request, id):
    thread = Comment.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", thread), content_type="application/json")

@csrf_exempt
def increment_replies(request):
    comment = Comment.objects.filter(pk=request.POST.get("id"))[0]
    comment.replies = comment.replies + 1
    comment.save()
    return HttpResponse("Success")

@csrf_exempt
def decrement_replies(request):
    comment = Comment.objects.filter(pk=request.POST.get("id"))[0]
    reply = int(request.POST.get("replies"))
    comment.replies = comment.replies - reply
    comment.save()
    return HttpResponse("Success")

@csrf_exempt
def create_thread(request):
    if request.method == "POST":
        user = request.user
        title = request.POST.get("title")
        content = request.POST.get("content")
        Comment.objects.create(author=user, is_thread=True, title=title, content=content)
    return HttpResponse("Success")

@csrf_exempt
def create_comment(request):
    if request.method == "POST":
        user = request.user
        parent = Comment.objects.filter(pk=request.POST.get("parent"))[0]
        content = request.POST.get("content")
        Comment.objects.create(author=user, parent=parent, is_thread=False, title='_', content=content)
    return HttpResponse("Success")

@csrf_exempt
def delete_comment(request):
    comment = Comment.objects.filter(pk=request.POST.get("id"))
    parent = comment.values()[0]['parent_id']
    replies = comment.values()[0]['replies']
    comment.delete()
    return HttpResponse(str(parent) + '_' + str(replies))

def get_child_comment(request):
    parent = Comment.objects.filter(pk=request.GET.get("parent"))[0]
    child_comment = Comment.objects.filter(parent=parent).order_by('replies', '-date')
    return HttpResponse(serializers.serialize("json", child_comment), content_type="application/json")
import json

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods


@login_required(login_url='accounts:login')
def user_profile(request, student_id):
    return render(request, 'accounts/user-profile.html',
                  {'this_student_id': student_id, 'is_edit': False})


@login_required(login_url='accounts:login')
def user_profile_edit(request, student_id):
    return render(request, 'accounts/user-profile.html',
                  {'this_student_id': student_id, 'is_edit': True})



@require_http_methods(['POST'])
def update_profile(request, student_id):
    user = request.user
    user.private_email = request.POST['email']
    user.mobile_phone = request.POST['phone']
    user.home_address = request.POST['address']
    if 'profile_pic' in request.FILES:
        user.profile_pic = request.FILES.get('profile_pic')
    user.save()
    return JsonResponse({'success': True})

@require_http_methods(['POST'])
def update_image(request, student_id):
    user = request.user
    print(request.FILES)
    if 'profile_pic' in request.FILES:
        user.profile_pic = request.FILES.get('profile_pic')
    user.save()
    return JsonResponse({'success': True})

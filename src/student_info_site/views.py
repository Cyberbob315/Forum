from django.shortcuts import render
from subforums.models import Subforum


def home_page(request):
    featured_subforums = Subforum.objects.all()[:8]
    return render(request, 'home.html', {'subforum_list': featured_subforums})

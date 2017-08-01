from django.shortcuts import render
from subforums.models import Subforum
from threads.models import Thread
from django.views.generic import ListView


def home_page(request):
    featured_subforums = Subforum.objects.all()[:8]
    return render(request, 'home.html', {'subforum_list': featured_subforums})


class SearchView(ListView):
    model = Thread
    template_name = 'search_page.html'


def search(request):
    return render(request, 'search_page.html', {})

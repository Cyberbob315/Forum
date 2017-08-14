from django.shortcuts import render
from subforums.models import Subforum


def home_page(request):
    featured_subforums = Subforum.objects.all()[:8]
    return render(request, 'home.html', {'subforum_list': featured_subforums})


def search(request):
    return render(request, 'search_page.html',
                  {'query': request.GET.get('query')})


def error_404(request):
    return render(request, 'error_404.html')


def error_403(request):
    return render(request, 'error_403.html')


def error_400(request):
    return render(request, 'error_400.html')

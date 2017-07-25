from django.shortcuts import render
from django.views.generic import ListView
from .models import Subforum


class SubforumListView(ListView):
    model = Subforum
    template_name = 'subforums/forum.html'
    context_object_name = 'subforum_list'



from re import template
from django.shortcuts import render
from django.views.generic import ListView

from base.models.books_models import Books


class IndexView(ListView):
    model = Books
    template_name = 'pages/index.html'
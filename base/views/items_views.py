from django.views.generic import ListView, View , DetailView

from base.models.books_models import Books


class IndexView(ListView):
    model = Books
    template_name = 'pages/index.html'


class BooksDetailView(DetailView):
    # /books/pk　で呼ばれ詳細画面を表示
    model = Books
    template_name='pages/book.html'    

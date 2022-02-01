from pyexpat import model
from django.views.generic import ListView, DetailView
from base.models import Order
import json

class OrderIndexView(ListView):
    model = Order
    template_name = 'pages/order_list.html'
    ordering= '-created_at'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user) #アクセスユーザの注文履歴だけ返す

class OrderDetailView(DetailView):
    model = Order
    template_name = 'pages/order.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user) #アクセスユーザの注文履歴だけ返す

    #contextに渡すときにjsonを変換しておく
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object() #OrderDetailクラスの渡されているmodel情報を取り出す
        context["books"] = json.loads(obj.books)
        context["shipping"] = json.loads(obj.shipping)
        return context
from typing import OrderedDict
from django.shortcuts import redirect
from django.views.generic import View, ListView

from base.models import Books
from config import settings

class CartListView(ListView):
    model = Books
    template_name = 'pages/cart.html'

    def get_queryset(self):
        #セッションのカートを取り出す
        cart = self.request.session.get('cart', None)
        #カートがなければリダイレクト
        if cart is None or len(cart) == 0 :
            redirect('/')
        #返却用querysetを再定義
        self.queryset = []
        #総計用変数をselfに追加
        self.total = 0
        #リスト用にデータを成形する
        for book_pk, quantity in cart['books'].items(): #itemsは辞書型のキーとバリューを取り出すメソッド
            obj = Books.objects.get(pk=book_pk)
            obj.quantity = quantity #量を追加
            obj.subtotal = int(obj.price * quantity) #合計金額 objに属性を追加
            self.queryset.append(obj) #Viewオブジェクトのローカルリストにobjを追加
            self.total += obj.subtotal #Viewオブジェクトに合計金額を追加
        self.tax_included_total = int(self.total * (settings.TAXRATE + 1)) #税込み金額を計算し追加
        cart['total'] = self.total #Viewオブジェクトからcartオブジェクトの辞書として追加
        cart['tax_included_total'] = self.tax_included_total
        self.request.session['cart'] = cart
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        #オーバーライドは先にしてしまう
        context = super().get_context_data(**kwargs)
        context['total'] = self.total #get_query_setでいれたtotalの値をcontextに渡す
        context['tax_included_total'] = self.tax_included_total
        return context


class AddCartView(View):
    #カートに追加orカートを生成
    def post(self,request):
        #隠しパラメータで送ってきたbook_pkを取る
        book_pk = request.POST.get("book_pk")
        #送ってきた量を取り出す。送られてきた時は文字列型
        quantity = int(request.POST.get('quantity'))
        #カートに追加するBookmodelを取ってくる
        book = Books.objects.filter(pk = book_pk)
        #セッションからキーでcartを取り出し
        cart = request.session.get('cart', None)
        #カートがなかった場合の処理
        if cart is None or len(cart) == 0 :
            #カートの初期化用、空の辞書型を作成。追加順で辞書型を生成するpython標準ライブラリを使用
            books = OrderedDict()
            cart = {'books': books}
        #カートがあり、[カートに追加]の商品が既にカートに存在する場合
        if book_pk in cart['books']:
            cart['books'][book_pk] += quantity
        else:
            cart['books'][book_pk] = quantity 
        
        #セッションのカートを更新
        request.session['cart'] = cart
        return redirect('/cart/')
    
def remove_from_cart(request,pk):
    cart = request.session.get('cart', None)
    if cart is not None:
        del cart['books'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')
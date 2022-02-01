from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import TemplateView, View
from django.conf import settings
import stripe
import json
from base.models import Books, Order


stripe.api_key = settings.STRIPE_API_SECRET_KEY

#stripeの税設定作成メソッドで税設定変数を作成
tax_rate = stripe.TaxRate.create(
    display_name = "消費税",
    description = "消費税",
    country = "JP",
    jurisdiction = "JP", #管轄を指定
    percentage = settings.TAXRATE *100,
    inclusive = False, #外税を指定
)

class PaySuccessView(TemplateView):
    template_name = 'pages/success.html'

    def get(self, request, *args, **kwargs):
        #最新のOrderオブジェクトを取得し注文確定に変更
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
        order.is_confirmed = True #注文確定
        order.save()  
        #カート情報削除
        del request.session['cart']

        return super().get(request, *args, **kwargs)

class PayCancelView(TemplateView):
    template_name = 'pages/cancel.html'

    def get(self, request, *args, **kwargs):
        #最新のOrderオブジェクトを取得し注文確定に変更
        order = Order.objects.filter(
            user=request.user).order_by('-created_at')[0]
        
        #在庫数と販売数をもとの状態に戻す
        for elem in json.loads(order.books):
            item = Books.objects.get(pk=elem['pk'])
            item.sold_count -= elem['quantity']
            item.stock += elem['quantity']
            item.save()

        #is_confirmedがFalseであれば削除（仮オーダー削除）
        if not order.is_confirmed:
            order.delete()

        return super().get(request, *args, **kwargs)


def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'jpy',
            'unit_amount': unit_amount,
            'product_data': {'name': name,},
        },
        'quantity': quantity,
        "tax_rates":[tax_rate.id],
    }


class PayWithStripe(View):
    
    def post(self,request,*args,**kwargs):
        
        #プロフィールのチェック

        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
        
        books = []
        line_items = []
        #カートを軸にループ
        for book_pk, quantity in cart['books'].items():
            book = Books.objects.get(pk=book_pk)
            line_item = create_line_item(
                book.price, book.name, quantity
            )
            line_items.append(line_item)

            # 注文履歴用のjsonファイル
            books.append({
                "pk": book.pk,
                "name": book.name,
                "image": str(book.image),
                "price": book.price,
                "quantity": quantity,
            })

            #modelの更新
            book.stock -= quantity
            book.sold_count += quantity
            book.save()

        #仮注文を作成(is_confirmed=False)
        Order.objects.create(
            user = request.user,
            uid = request.user.pk,
            books = json.dumps(books),
            shipping = "",
            amount = cart['total'],
            tax_included = cart['tax_included_total']
        )
        
        #Stripeの決済ページへのセッションを作成
        checkout_session = stripe.checkout.Session.create(
            customer_email = request.user.email,
            payment_method_types = ['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url = f'{settings.MY_URL}/pay/cancel',
        )
        return redirect(checkout_session.url)

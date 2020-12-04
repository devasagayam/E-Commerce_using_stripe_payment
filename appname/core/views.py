from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View,CreateView,UpdateView,TemplateView,DeleteView
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile,Rating,Contact
from django.urls import reverse_lazy
from . import forms,models
from django.contrib.auth import get_user_model
from django.db.models import Q
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib.auth.models import User

import random
import string
import stripe

from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
now = datetime.now()
dd=now + timedelta(days=2)
ddd=now + timedelta(days=3)
x=False

# Create your views here.
class delete_product(DeleteView):
    model=Item
    template_name='delete.html'
    success_url=reverse_lazy("core:stock")


def cont(request):

    if request.method=='POST':

        name=request.POST.get("name")
        email=request.POST.get("email")
        sub=request.POST.get("subject")
        msg=request.POST.get("msg")
        cont=Contact()
        cont.name=name
        cont.email=email
        cont.subject=sub
        cont.message=msg
        cont.save()
        return redirect("core:cont")
    return render(request,'conat.html')

@csrf_exempt
def coment(request,slug):
    global now
    item=Item.objects.get(slug=slug)
    try:
        create_rating=Rating.objects.get(user=request.user,item=item)
    except ObjectDoesNotExist:
        create_rating=''

    if request.method=='POST':
        coment=request.POST.get("comment")
        if create_rating:
            create_rating.comment=coment
            create_rating.time=now
            create_rating.save()
        else:
            create_rating=Rating()
            create_rating.user=request.user
            create_rating.item=item
            create_rating.comment=coment
            create_rating.time=now
            create_rating.save()
        return redirect('core:product',slug=slug)


@csrf_exempt
def rating(request,slug):
    item=Item.objects.get(slug=slug)
    try:
        create_rating=Rating.objects.get(user=request.user,item=item)
    except ObjectDoesNotExist:
        create_rating=''

    if request.method=='POST':
        ra=int(request.POST.get("rating"))
        width=(ra*100)/5
        if create_rating:
            create_rating.rating=ra
            create_rating.width=width
            create_rating.save()
        else:
            create_rating=Rating()
            create_rating.user=request.user
            create_rating.item=item
            create_rating.rating=ra
            create_rating.width=width
            create_rating.save()
        return redirect('core:product',slug=slug)

def ItemDetailView(request,slug):
    object=Item.objects.get(slug=slug)
    ratings=Rating.objects.filter(item=object)
    j=0

    for i in ratings:
        if i.comment:
            j+=1

    l=int(len(ratings))
    sum=0
    avg=0
    rating=0
    for rating in ratings:
        sum+=rating.rating
    if l>0:
        avg=sum/l
    else:
        avg=0
    width=(avg*100)/5


    avg=format(avg, '.1f')




    return render(request,'product.html',{'object':object,'l':l,'width':width,'avg':avg,'ratings':ratings,'j':j})


now = datetime.now()
dd=now + timedelta(days=2)
ddd=now + timedelta(days=3)
x=False

stripe.api_key = settings.STRIPE_SECRET_KEY

"""
class profilecreation(CreateView):
    form_class=profileform
    success_url='home'
    template_name='profile.html'
 """
class faq(TemplateView):
    template_name='faq.html'

class ps(TemplateView):
    template_name='ps.html'

def refaccept(request,slug):
    global ddd
    order=get_object_or_404(Order, ref_code=slug)
    ref=get_object_or_404(Refund, trid=slug)
    mail_subject = 'Your refund request aprooved .'
    message = render_to_string('rfacpt.html', {
        'product': order,
        'ddd': ddd,
    })
    to_email =ref.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    order.refund_granted=True
    order.refund_requested=False
    order.save()
    return  redirect('core:refrq')


def refreject(request,slug):
    global ddd
    order=get_object_or_404(Order, ref_code=slug)
    ref=get_object_or_404(Refund, trid=slug)
    mail_subject = 'Your Refund Request dis-aprooved .'
    message = render_to_string('rfrjct.html', {
        'product': order,
        'ddd': ddd,
    })
    to_email =ref.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    order.refund_granted=True
    order.refund_requested=False
    order.save()
    return  redirect('core:refrq')


def viewref(request,pk):
    product= get_object_or_404(Order, pk=pk)
    tid=product.ref_code
    ref=get_object_or_404(Refund, trid=tid)
    return render(request,'refview.html',{'ref':ref})


class updatestock(UpdateView):
    model=models.Item
    fields='__all__'
    success_url=reverse_lazy('core:stock')
    template_name='updatestock.html'

def remainder(request,pk):
    global dd
    product= get_object_or_404(OrderItem, pk=pk)
    mail_subject = 'Remainder to return the product.'
    message = render_to_string('rtx.html', {
        'product': product,
        'dd': dd,
    })
    to_email =product.user.email
    email = EmailMessage(
                mail_subject, message, to=[to_email]
    )
    email.send()
    return  redirect('core:recover')


def action(request,pk):
    order=OrderItem.objects.get(id=pk)
    order.action=True
    order.save()
    return redirect('core:uproduct')




"""class uproduct(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = OrderItem.objects.filter(user=self.request.user, ordered=True,action=False).order_by('due_date')
            context = {
                'object': order
            }
            return render(self.request, 'uproduct.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:home")"""

class uproduct(ListView):
    template_name='uproduct.html'
    context_object_name='object'
    paginate_by = 5

    def get_queryset(self):
        queryset=OrderItem.objects.filter(user=self.request.user, ordered=True,action=False).order_by('due_date')
        return queryset

"""def recover(request):
    global now
    order = OrderItem.objects.filter(due_date__lt=now.date(), ordered=True,action=False)
    context = {
        'object': order
    }
    return render(request, 'recover.html', context)"""

class recover(ListView):
    queryset=OrderItem.objects.filter(due_date__lt=now.date(), ordered=True,action=False)
    template_name='recover.html'
    context_object_name='object'
    paginate_by = 5




"""class utransaction(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=True).order_by('-ordered_date')
            context = {
                'info': order
            }
            return render(self.request, 'utransaction.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have any Transactions")
            return redirect("core:home")"""

class utransaction(ListView):
    template_name='utransaction.html'
    context_object_name='info'
    paginate_by = 10

    def get_queryset(self):
        queryset=Order.objects.filter(user=self.request.user, ordered=True).order_by('-ordered_date')
        return queryset




"""def transaction(request):
    info=Order.objects.filter(ordered=True).order_by('-ordered_date')
    return render(request,'transaction.html',{'info':info})"""

class transaction(ListView):
    queryset=Order.objects.filter(ordered=True).order_by('-ordered_date')
    template_name='transaction.html'
    context_object_name='info'
    paginate_by = 10


"""def refrq(request):
    info=Order.objects.filter(ordered=True,refund_requested=True,refund_granted=False).order_by('-ordered_date')
    return render(request,'rfrq.html',{'info':info})"""

class refrq(ListView):
    queryset=Order.objects.filter(ordered=True,refund_requested=True,refund_granted=False).order_by('-ordered_date')
    template_name='rfrq.html'
    context_object_name='info'
    paginate_by = 5


class addstock(CreateView):
    form_class =forms.addform
    template_name = 'addstock.html'
    model = models.Item
    success_url=reverse_lazy('core:home')



def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

"""def stock(request):
    context = {
        'objects': Item.objects.all()
    }
    return render(request, "stock.html", context)"""

class stock(ListView):
    queryset=Item.objects.all()
    template_name='stock.html'
    context_object_name='objects'
    paginate_by = 10



def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        ra=0
        item=Item.objects.get(pk=1)
        ra=Rating.objects.filter(item=item)
        l=len(ra)
        sum=0
        for rating in ra:
            sum+=rating.rating
        if l>0:
            print(sum/l)
        else:
            print(0)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()

            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_country = form.cleaned_data.get(
                        'shipping_country')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_country, shipping_zip]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            country=shipping_country,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('core:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_country = form.cleaned_data.get(
                        'billing_country')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_country, billing_zip]):
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            country=billing_country,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("core:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False
            }
            userprofile = self.request.user.userprofile
            if userprofile.one_click_purchasing:
                # fetch the users card list
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id,
                    limit=3,
                    object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    # update the context with the default card
                    context.update({
                        'card': card_list[0]
                    })
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("core:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = PaymentForm(self.request.POST)
        userprofile = UserProfile.objects.get(user=self.request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    stripe.Customer.modify(userprofile.stripe_customer_id,
                    source=token)
                else:
                    customer = stripe.Customer.create(
                        email=self.request.user.email
                    )
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:

                if use_default or save:
                    # charge the customer because we cannot charge the token more than once
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="INR",
                        customer=userprofile.stripe_customer_id
                    )
                else:
                    # charge once off on the token
                    charge = stripe.Charge.create(
                        amount=amount,  # cents
                        currency="INR",
                        source=token
                    )

                #invice
                ref=create_ref_code()

                # create the payment
                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = self.request.user
                payment.receipt=True
                payment.amount = order.get_total()
                payment.save()

                # assign the payment to the order
                #invice
                context1= {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'd':now,
                    'ref':ref
                }
                mail_subject="Invoice From Tarrif"
                u=User.objects.get(username=self.request.user)
                to=u.email
                message=render_to_string('invice.html',context1)
                finalmessage=strip_tags(message)
                email=EmailMultiAlternatives(mail_subject,finalmessage,settings.EMAIL_HOST_USER,to=[to])
                email.attach_alternative(message,"text/html")
                email.send()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = ref
                order.save()
                messages.success(self.request, "Your order was successful!")
                return redirect("accounts:pay")





            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(self.request, f"{err.get('message')}")
                return redirect("/")

            except stripe.error.RateLimitError as e:
                # Too many requests made to the API too quickly
                messages.warning(self.request, "Rate limit error")
                return redirect("/")

            except stripe.error.InvalidRequestError as e:
                # Invalid parameters were supplied to Stripe's API
                print(e)
                messages.warning(self.request, "Invalid parameters")
                return redirect("/")

            except stripe.error.AuthenticationError as e:
                # Authentication with Stripe's API failed
                # (maybe you changed API keys recently)
                messages.warning(self.request, "Not authenticated")
                return redirect("/")

            except stripe.error.APIConnectionError as e:
                # Network communication with Stripe failed
                messages.warning(self.request, "Network error")
                return redirect("/")

            except stripe.error.StripeError as e:
                # Display a very generic error to the user, and maybe send
                # yourself an email
                messages.warning(
                    self.request, "Something went wrong. You were not charged. Please try again.")
                return redirect("/")

            except Exception as e:
                # send an email to ourselves
                messages.warning(
                    self.request, "A serious error occurred. We have been notifed.")
                return redirect("/")

        messages.warning(self.request, "Invalid data received")
        return redirect("/payment/stripe/")



class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

class party(ListView):
    queryset=Item.objects.filter(category='OW')
    model = Item
    paginate_by = 5
    template_name = "party.html"


@csrf_exempt
def costume(request):
    q=None
    products=''
    try:
        q=request.GET.get('s')

        print(q)
    except:
        q=None
    if q:
        products=Item.objects.filter(title__icontains=q)
        context={'query':q,'products':products}
        template='costume.html'
    else:
        template='costume.html'
        context={}
    for i in products:
        print(i)
    return render(request,template,context)



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order,
                'couponform': CouponForm(),

            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")






@login_required
def increasedays(request,slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.rentdays += 1
            dd=order_item.due_date
            order_item.due_date=dd + timedelta(days=1)
            order_item.save()
            messages.info(request, "This item Rent Days  was updated.")
            return redirect("core:order-summary")
    else:
        print("eror")

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def decreasedays(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False #ffd
            )[0]
            if order_item.rentdays > 1:
                order_item.rentdays -= 1
                dd=order_item.due_date
                order_item.due_date=dd - timedelta(days=1)
                order_item.save()
            messages.info(request, "This item Rent days was updated.")
            return redirect("core:order-summary")


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False #ffd
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


def get_coupon(request, code):
    global x
    try:
        coupon = Coupon.objects.get(code=code)
        x=True
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exist")
        return redirect("core:checkout")


class AddCouponView(View):


    def post(self, *args, **kwargs):
        global x
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                c= get_coupon(self.request, code)
                print(x)
                if x:
                    print(x)
                    order.coupon =c
                    order.save()
                    x=False
                    messages.success(self.request, "Successfully added coupon")
                    return redirect("core:order-summary")
                else:

                    return redirect("core:order-summary")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("core:checkout")


class RequestRefundView(View):
    def get(self, *args, **kwargs):
        form = RefundForm()
        context = {
            'form': form
        }
        return render(self.request, "request_refund.html", context)

    def post(self, *args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                check=order.refund_granted
                if check == False:
                    order.refund_requested = True
                    order.save()

                    # store the refund
                    refund = Refund()
                    refund.trid=ref_code
                    refund.order = order
                    refund.reason = message
                    refund.email = email
                    refund.save()
                    messages.info(self.request, "Your request was received.")
                    return redirect("core:request-refund")

                else:
                    messages.info(self.request, "You already recieved refund for this transaction.")
                    return redirect("core:request-refund")

            except ObjectDoesNotExist:
                messages.info(self.request, "This order does not exist.")
                return redirect("core:request-refund")

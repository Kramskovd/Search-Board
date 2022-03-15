from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Product, Category, ThingCategory
from django.template import loader
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView
from .forms import ProductForm, ChangeUserInfoForm
from .forms import RegisterUserForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.core.signing import BadSignature
from django.views.generic.base import TemplateView
from .models import AdvUser
from django.core import serializers
from .utilities import signer
import json
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView, login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.core.paginator import Paginator


class SebLoginView(LoginView):
    template_name = 'seboapp/account/login.html'
    success_url = 'google.com'


def delete_product(request):
    if request.method == 'GET':
        pk = request.GET['pk']
        product = Product.objects.get(pk=pk)
        product.delete()
        return HttpResponseRedirect(reverse_lazy('sebo:profile'))


def category_filter(request):
    if request.method == 'GET':
        template = loader.get_template('seboapp/index.html')
        categories = Category.objects.order_by()

        filters = request.GET
        price_max = Product.objects.aggregate(Max('price'))['price__max']
        full_path = request.get_full_path()

        if filters['price_to'] != '':
            price_max = filters['price_to']

        sort = filters['sort']
        if sort == 'date':
            sort = 'по дате'
            sort_type = '-date_published'
        else:
            sort = 'по цене'
            sort_type = 'price'

        if int(filters['category']) != -1:
            name_category = Category.objects.get(pk=filters['category']).name_category
        else:
            name_category = 'не выбрано'
        if int(filters['thing']) != -1:
            name_thing = ThingCategory.objects.get(pk=filters['thing']).name_thing
            products = Product.objects.filter(thing_category_id=filters['thing'],
                                              price__gte=filters['price_from'],
                                              price__lte=price_max).order_by(sort_type)
        else:
            name_thing = 'не выбрано'
            products = Product.objects.filter(price__gte=filters['price_from'], price__lte=price_max).order_by(sort_type)

        paginator = Paginator(products, 2)

        if 'page' in request.GET:
            page_num = request.GET['page']
        else:
            page_num = 1

        page = paginator.get_page(page_num)

        context = {'products': page.object_list, 'page': page, 'full_path': full_path,
                   'categories': categories, 'name_category': name_category, 'name_thing': name_thing,
                   'price_from': filters['price_from'], 'price_to': filters['price_to'], 'sort': sort}

        return HttpResponse(template.render(context, request))


def get_category(request):
    if request.method == 'GET':
        id_category = request.GET['id']
        c = Category.objects.get(pk=id_category)
        thingcategory = {"res": list(c.thingcategory_set.values('id', 'name_thing'))}

        return HttpResponse(json.dumps(thingcategory, ensure_ascii=False), content_type="application/json")


def product_profile(request, pk):
    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        context = {'product': product}
        return render(request, template_name='seboapp/call.html', context=context)
    else:
        return HttpResponseRedirect(reverse_lazy('sebo:index'))


@login_required
def profile(request):
    products = Product.objects.filter(user=request.user.pk).all()
    context = {'products': products}
    return render(request, template_name='seboapp/account/profile.html', context=context)


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = AdvUser
    template_name = 'seboapp/account/change_info_user.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('sebo:profile')
    success_message = 'Данные успешно обновлены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
            return get_object_or_404(queryset, pk=self.user_id)


class SeboPasswordChangeView(PasswordChangeView, SuccessMessageMixin, LoginRequiredMixin):
    template_name = 'seboapp/account/password_change.html'
    success_url = reverse_lazy('sebo:profile')
    success_message = 'Пароль изменился'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'main/bad_signature.html')

    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template = 'main/user_is_activated.html'
    else:
        template = 'main/activation_done.html'
        user.is_activate = True
        user.is_activated = True
        user.save()

    return render(request, template)


def index(request):
    template = loader.get_template('seboapp/index.html')
    products = Product.objects.order_by('-date_published')
    paginator = Paginator(products, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    categories = Category.objects.order_by()
    context = {'products': page.object_list, 'page': page, 'categories': categories,
               'name_category': 'не выбрано', 'name_thing': 'не выбрано',
               'price_from': 0, 'price_to': '', 'sort': 'по дате'
               }
    return HttpResponse(template.render(context, request))


class SLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'seboapp/account/logout.html'


class RegisterDoneView(TemplateView):
    template_name = 'seboapp/account/register_done.html'


class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'seboapp/account/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('sebo:register_done')


@login_required
def add_production(request):
    if request.method == 'POST':
        pf = ProductForm(request.POST, request.FILES, initial={'user': request.user.pk})
        if pf.is_valid():

            pf.save()
            return HttpResponseRedirect(reverse_lazy('sebo:index'))
        else:
            context = {'form': pf}
            return render(request, 'seboapp/add.html', context)
    else:
        pf = ProductForm(initial={'user': request.user.pk})

        pf.save(commit=False)
        context = {'form': pf}
        return render(request, 'seboapp/add.html', context)


class AddProductView(CreateView):
    template_name = 'seboapp/add.html'
    form_class = ProductForm
    success_url = reverse_lazy('sebo:index')

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from .forms import CreateProductForm, UpdateProductForm
from .models import Category, Product

class SearchListView(ListView):
    model = Product
    template_name = 'search.html'
    context_object_name = 'results'

    def get_queryset(self):
        queryset = super().get_queryset()
        print(self.request.GET)
        search_word = self.request.GET.get('q')
        if not search_word:
            queryset = Product.objects.none()
        else:
            queryset = Product.objects.filter(Q(name__icontains=search_word) | Q(description__icontains=search_word))

        return queryset


class CategoryListView(ListView):
    model = Category            #categories = Category.objects.all()
    template_name = 'home.html'
    context_object_name = 'categories'

class ProductListView(ListView):
    model = Product         #Product.object.all()
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        slug = self.kwargs.get('slug')
        # print(self.kwargs)
        queryset = queryset.filter(category__slug=slug)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'detail.html'
    context_object_name = 'product'
    pk_url_kwarg = 'product_id'

class IsAdminCheckMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser



class ProductCreateView(IsAdminCheckMixin, CreateView):
    model = Product
    template_name = 'create_product.html'
    form_class = CreateProductForm
    # context_object_name = 'product_form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductUpdateView(IsAdminCheckMixin, UpdateView):
    model = Product
    template_name = 'update_product.html'
    form_class = UpdateProductForm
    pk_url_kwarg = 'product_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.get_form_class())
        return context


class ProductDeleteView(IsAdminCheckMixin, DeleteView):
    model = Product
    template_name = 'delete_product.html'
    pk_url_kwarg = 'product_id'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        slug = self.object.category.slug
        self.object.delete()
        return redirect('list', slug)

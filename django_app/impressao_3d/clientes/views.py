from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Cliente
from .forms import ClienteForm

# Create your views here.



class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q       = self.request.GET.get('q', '')
        estagio = self.request.GET.get('estagio', '')
        tipo    = self.request.GET.get('tipo', '')

        if q:
            qs = qs.filter(
                Q(nome__icontains=q) |
                Q(whatsapp__icontains=q) |
                Q(instagram__icontains=q)
            )
        if estagio:
            qs = qs.filter(estagio=estagio)
        if tipo:
            qs = qs.filter(tipo=tipo)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['estagios'] = Cliente.Estagio.choices
        ctx['tipos']    = Cliente.Tipo.choices
        ctx['q']        = self.request.GET.get('q', '')
        ctx['estagio_sel'] = self.request.GET.get('estagio', '')
        ctx['tipo_sel']    = self.request.GET.get('tipo', '')
        return ctx


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/detalhe.html'
    context_object_name = 'cliente'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['orcamentos'] = self.object.orcamentos.order_by('-data_criacao') # type: ignore
        return ctx


class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = 'Novo Cliente'
        return ctx


class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/form.html'
    success_url = reverse_lazy('clientes:lista')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['titulo'] = f'Editar — {self.object.nome}' # type: ignore
        return ctx
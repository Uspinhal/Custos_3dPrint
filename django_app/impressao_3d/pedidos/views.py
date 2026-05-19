from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory

from .models import Pedido, ItemPedido, OrdemProducao, OrdemProducaoItem
from .forms import PedidoForm, ItemPedidoForm, OrdemProducaoForm, OrdemProducaoItemStatusForm


# ---------------------------------------------------------------------------
# Formset de itens — usado em novo_pedido e editar_pedido
# ---------------------------------------------------------------------------

ItemPedidoFormSet = inlineformset_factory(
    Pedido, ItemPedido,
    form=ItemPedidoForm,
    extra=1,
    can_delete=True,
)


# ===========================================================================
# PEDIDOS
# ===========================================================================

def lista_pedidos(request):
    pedidos = Pedido.objects.select_related('cliente').order_by('-data_pedido', '-prioridade')

    # Filtros opcionais via GET
    origem = request.GET.get('origem', '')
    status = request.GET.get('status', '')

    if origem:
        pedidos = pedidos.filter(origem=origem)

    # status é @property — filtra em Python após queryset
    if status:
        pedidos = [p for p in pedidos if p.status == status]

    return render(request, 'pedidos/lista.html', {
        'pedidos': pedidos,
        'origem_sel': origem,
        'status_sel': status,
        'origens': Pedido.ORIGEM_CHOICES,
        'status_opcoes': list(Pedido.STATUS_LABELS.items()),
    })


def novo_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        formset = ItemPedidoFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            pedido = form.save()
            formset.instance = pedido
            formset.save()
            messages.success(request, f'Pedido #{pedido.pk} criado com sucesso.')
            return redirect('pedidos:detalhe', pedido_id=pedido.pk)
    else:
        form = PedidoForm()
        formset = ItemPedidoFormSet()

    return render(request, 'pedidos/form.html', {
        'form': form,
        'formset': formset,
        'titulo': 'Novo Pedido',
    })


def detalhe_pedido(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related('cliente', 'orcamento'),
        pk=pedido_id,
    )
    itens = pedido.itens.all()  # type: ignore[attr-defined]

    return render(request, 'pedidos/detalhe.html', {
        'pedido': pedido,
        'itens': itens,
    })


def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)

    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        formset = ItemPedidoFormSet(request.POST, instance=pedido)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f'Pedido #{pedido.pk} atualizado.')
            return redirect('pedidos:detalhe', pedido_id=pedido.pk)
    else:
        form = PedidoForm(instance=pedido)
        formset = ItemPedidoFormSet(instance=pedido)

    return render(request, 'pedidos/form.html', {
        'form': form,
        'formset': formset,
        'titulo': f'Editar Pedido #{pedido.pk}',
        'pedido': pedido,
    })


def marcar_enviado(request, pedido_id):
    """Único status manual — marca o pedido como enviado após postagem."""
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    if request.method == 'POST':
        pedido.is_enviado = True
        pedido.save()
        messages.success(request, f'Pedido #{pedido.pk} marcado como enviado.')
    return redirect('pedidos:detalhe', pedido_id=pedido.pk)


# ===========================================================================
# ORDENS DE PRODUÇÃO
# ===========================================================================

def _itens_disponiveis(tipo_impressao=None):
    """
    Itens que ainda não foram concluídos nem estão imprimindo em nenhuma OP.
    Critério: não existe OrdemProducaoItem com status 'imprimindo' ou 'concluido'
    para aquele item.
    """
    excluir = OrdemProducaoItem.objects.filter(
        status__in=['imprimindo', 'concluido']
    ).values_list('item_id', flat=True)

    qs = (
        ItemPedido.objects
        .exclude(pk__in=excluir)
        .select_related('pedido', 'pedido__cliente')
        .order_by('-pedido__prioridade', 'pedido__data_prazo', 'pedido__data_pedido')
    )

    if tipo_impressao:
        qs = qs.filter(tipo_impressao=tipo_impressao)

    return qs


def lista_ordens(request):
    ordens = OrdemProducao.objects.select_related('impressora', 'materia_prima').order_by('-id')
    return render(request, 'pedidos/ordens/lista.html', {'ordens': ordens})


def nova_ordem(request):
    tipo = request.GET.get('tipo', 'resina')  # filtro primário — padrão resina
    itens_disponiveis = _itens_disponiveis(tipo_impressao=tipo)

    if request.method == 'POST':
        form = OrdemProducaoForm(request.POST)
        itens_selecionados = request.POST.getlist('itens')

        if form.is_valid():
            if not itens_selecionados:
                messages.error(request, 'Selecione pelo menos um item.')
            else:
                ordem = form.save()
                for item_id in itens_selecionados:
                    item = get_object_or_404(ItemPedido, pk=item_id)
                    OrdemProducaoItem.objects.create(ordem=ordem, item=item)
                messages.success(request, f'{ordem} criada com {len(itens_selecionados)} item(s).')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)
        # se form inválido, mantém tipo e itens disponíveis para reexibir
        tipo = request.POST.get('tipo_impressao_filtro', tipo)
        itens_disponiveis = _itens_disponiveis(tipo_impressao=tipo)

    else:
        form = OrdemProducaoForm()

    return render(request, 'pedidos/ordens/form_nova.html', {
        'form': form,
        'itens_disponiveis': itens_disponiveis,
        'tipo_sel': tipo,
        'tipos': ItemPedido.TIPO_IMPRESSAO_CHOICES,
    })


def detalhe_ordem(request, ordem_id):
    ordem = get_object_or_404(
        OrdemProducao.objects.select_related('impressora', 'materia_prima'),
        pk=ordem_id,
    )
    op_itens = (
        ordem.op_itens  # type: ignore[attr-defined]
        .select_related('item', 'item__pedido', 'item__pedido__cliente')
        .order_by('item__pedido__id')
    )

    # Formulários de status individuais por OrdemProducaoItem
    if request.method == 'POST':
        op_item_id = request.POST.get('op_item_id')
        op_item = get_object_or_404(OrdemProducaoItem, pk=op_item_id, ordem=ordem)
        status_form = OrdemProducaoItemStatusForm(request.POST, instance=op_item)

        if status_form.is_valid():
            # Bloqueia fechamento se quantidade_utilizada não preenchida
            novo_status = status_form.cleaned_data['status']
            if novo_status == 'concluido':
                todos_concluidos_apos = not (
                    ordem.op_itens  # type: ignore[attr-defined]
                    .exclude(pk=op_item.pk)
                    .exclude(status='concluido')
                    .exists()
                )
                if todos_concluidos_apos and not ordem.quantidade_utilizada:
                    messages.error(
                        request,
                        'Preencha a quantidade utilizada da OP antes de concluir o último item.'
                    )
                    return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            status_form.save()
            messages.success(request, f'Status atualizado para "{op_item.get_status_display()}".')  # type: ignore[attr-defined]
        return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

    status_forms = {
        oi.pk: OrdemProducaoItemStatusForm(instance=oi)
        for oi in op_itens
    }

    return render(request, 'pedidos/ordens/detalhe.html', {
        'ordem': ordem,
        'op_itens': op_itens,
        'status_forms': status_forms,
    })


def editar_ordem(request, ordem_id):
    ordem = get_object_or_404(OrdemProducao, pk=ordem_id)

    if request.method == 'POST':
        form = OrdemProducaoForm(request.POST, instance=ordem)
        if form.is_valid():
            form.save()
            messages.success(request, f'{ordem} atualizada.')
            return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)
    else:
        form = OrdemProducaoForm(instance=ordem)

    return render(request, 'pedidos/ordens/form_editar.html', {
        'form': form,
        'ordem': ordem,
    })
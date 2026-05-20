from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms import inlineformset_factory
from django.utils import timezone

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
    prioridade = request.GET.get('prioridade', '')
    enviado = request.GET.get('enviado', '')
    status = request.GET.get('status', '')

    if origem:
        pedidos = pedidos.filter(origem=origem)
    if prioridade:
        pedidos = pedidos.filter(prioridade=prioridade)
    if enviado == '0':
        pedidos = pedidos.filter(is_enviado=False)
    elif enviado == '1':
        pedidos = pedidos.filter(is_enviado=True)

    # status é @property — filtra em Python após queryset
    if status:
        pedidos = [p for p in pedidos if p.status == status]

    return render(request, 'pedidos/lista.html', {
        'pedidos': pedidos,
        'filtros': {
            'origem': origem,
            'prioridade': prioridade,
            'enviado': enviado,
            'status': status,
        },
        'origem_choices': Pedido.ORIGEM_CHOICES,
        'prioridade_choices': Pedido.PRIORIDADE_CHOICES,
        'status_opcoes': list(Pedido.STATUS_LABELS.items()),
        'today': timezone.localdate(),
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
        'action': 'criar',
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
        'action': 'editar',
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

def _itens_disponiveis(tipo_impressao=None, excluir_ordem_id=None):
    """
    Itens que ainda não foram concluídos nem estão imprimindo em nenhuma OP.
    Critério: não existe OrdemProducaoItem com status 'imprimindo' ou 'concluido'
    para aquele item.
    """
    excluir_qs = OrdemProducaoItem.objects.filter(
        status__in=['imprimindo', 'concluido']
    )

    if excluir_ordem_id:
        excluir_qs = excluir_qs | OrdemProducaoItem.objects.filter(ordem_id=excluir_ordem_id)

    excluir = excluir_qs.values_list('item_id', flat=True)

    qs = (
        ItemPedido.objects
        .exclude(pk__in=excluir)
        .select_related('pedido', 'pedido__cliente')
        .order_by('-pedido__prioridade', 'pedido__data_prazo', 'pedido__data_pedido')
    )

    if tipo_impressao:
        qs = qs.filter(tipo_impressao=tipo_impressao)

    return qs


def _alocar_item_na_ordem(ordem, item_id):
    """
    Move automaticamente vínculos abertos/falhados do item para a OP atual.
    Vínculos concluídos ou imprimindo são preservados.
    """
    OrdemProducaoItem.objects.filter(
        item_id=item_id,
        status__in=['na_fila', 'falhou'],
    ).exclude(ordem=ordem).delete()

    op_item, created = OrdemProducaoItem.objects.get_or_create(
        ordem=ordem,
        item_id=item_id,
        defaults={'status': 'na_fila'},
    )
    return op_item, created


def lista_ordens(request):
    ordens = OrdemProducao.objects.select_related('impressora', 'materia_prima').order_by('-id')
    return render(request, 'pedidos/ordens/lista.html', {'ordens': ordens})


def nova_ordem(request):
    tipo = request.GET.get('tipo_impressao', 'resina')  # filtro primário — padrão resina
    itens_disponiveis = _itens_disponiveis(tipo_impressao=tipo)
    itens_selecionados = []

    if request.method == 'POST':
        form = OrdemProducaoForm(request.POST)
        itens_selecionados = request.POST.getlist('item_ids')

        if form.is_valid():
            if not itens_selecionados:
                messages.error(request, 'Selecione pelo menos um item.')
            else:
                ordem = form.save()
                for item_id in itens_selecionados:
                    item = get_object_or_404(ItemPedido, pk=item_id)
                    _alocar_item_na_ordem(ordem, item.pk)
                messages.success(request, f'{ordem} criada com {len(itens_selecionados)} item(s).')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)
        # se form inválido, mantém tipo e itens disponíveis para reexibir
        tipo = request.POST.get('tipo_impressao_filtro', tipo)
        itens_disponiveis = _itens_disponiveis(tipo_impressao=tipo)

    else:
        form = OrdemProducaoForm()

    return render(request, 'pedidos/ordens/form_nova.html', {
        'form': form,
        'itens_qs': itens_disponiveis,
        'tipo_filtro': tipo,
        'tipo_choices': ItemPedido.TIPO_IMPRESSAO_CHOICES,
        'selected_item_ids': itens_selecionados,
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
        action = request.POST.get('action', 'status')

        if action == 'add_items':
            if ordem.data_conclusao:
                messages.error(request, 'Esta OP já foi finalizada e não pode receber novos itens.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            itens_selecionados = request.POST.getlist('item_ids')
            if not itens_selecionados:
                messages.error(request, 'Selecione pelo menos um item para adicionar.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            itens_disponiveis_ids = set(
                _itens_disponiveis(excluir_ordem_id=ordem.pk)
                .values_list('id', flat=True)
            )
            adicionados = 0

            for item_id in itens_selecionados:
                try:
                    item_id_int = int(item_id)
                except (TypeError, ValueError):
                    continue

                if item_id_int not in itens_disponiveis_ids:
                    continue

                _, created = _alocar_item_na_ordem(ordem, item_id_int)
                if created:
                    adicionados += 1

            if adicionados:
                messages.success(request, f'{adicionados} item(ns) adicionados à {ordem}.')
            else:
                messages.warning(request, 'Nenhum item pôde ser adicionado a esta OP.')
            return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

        if action == 'finalizar':
            if ordem.data_conclusao:
                messages.info(request, f'{ordem} já estava finalizada.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            if not ordem.op_itens.exists():  # type: ignore[attr-defined]
                messages.error(request, 'Não é possível finalizar uma OP sem itens.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            if ordem.op_itens.exclude(status='concluido').exists():  # type: ignore[attr-defined]
                messages.error(request, 'Todos os itens precisam estar concluídos para finalizar a OP.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            quantidade_utilizada = request.POST.get('quantidade_utilizada')
            if quantidade_utilizada in (None, ''):
                messages.error(request, 'Preencha a quantidade utilizada antes de finalizar a OP.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            try:
                quantidade_utilizada_float = float(quantidade_utilizada.replace(',', '.'))
            except ValueError:
                messages.error(request, 'Informe uma quantidade utilizada válida.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            if quantidade_utilizada_float <= 0:
                messages.error(request, 'A quantidade utilizada precisa ser maior que zero.')
                return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            ordem.quantidade_utilizada = quantidade_utilizada_float
            ordem.data_conclusao = timezone.now()
            ordem.save(update_fields=['quantidade_utilizada', 'data_conclusao'])
            messages.success(request, f'{ordem} finalizada com sucesso.')
            return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

        if ordem.data_conclusao:
            messages.error(request, 'Esta OP já foi finalizada e não permite alterar status de itens.')
            return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

        op_item_id = request.POST.get('op_item_id')
        op_item = get_object_or_404(OrdemProducaoItem, pk=op_item_id, ordem=ordem)
        status_form = OrdemProducaoItemStatusForm(request.POST, instance=op_item)

        if status_form.is_valid():
            novo_status = status_form.cleaned_data['status']
            if novo_status == 'imprimindo':
                if ordem.impressora.em_manutencao:
                    messages.error(
                        request,
                        f'{ordem.impressora.nome} está em manutenção e não pode iniciar impressão.'
                    )
                    return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

                op_concorrente = (
                    OrdemProducao.objects
                    .filter(
                        impressora=ordem.impressora,
                        data_conclusao__isnull=True,
                        op_itens__status='imprimindo',
                    )
                    .exclude(pk=ordem.pk)
                    .distinct()
                    .first()
                )
                if op_concorrente:
                    messages.error(
                        request,
                        f'{ordem.impressora.nome} já está imprimindo {op_concorrente}.'
                    )
                    return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

            status_form.save()
            messages.success(request, f'Status atualizado para "{op_item.get_status_display()}".')  # type: ignore[attr-defined]
        return redirect('pedidos:detalhe_ordem', ordem_id=ordem.pk)

    op_item_forms = [
        {'op_item': oi, 'form': OrdemProducaoItemStatusForm(instance=oi)}
        for oi in op_itens
    ]
    itens_disponiveis = _itens_disponiveis(excluir_ordem_id=ordem.pk)

    return render(request, 'pedidos/ordens/detalhe.html', {
        'ordem': ordem,
        'op_itens': op_itens,
        'op_item_forms': op_item_forms,
        'itens_disponiveis': itens_disponiveis,
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

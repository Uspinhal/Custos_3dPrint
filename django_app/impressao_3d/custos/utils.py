from datetime import date
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima, Insumos

class CalculadoraCustos:
    def __init__(self, equipamento_id, tempo_horas):
        self.equipamento = Equipamento.objects.get(id=equipamento_id)
        self.tempo_horas = tempo_horas

    def custo_manutencao(self):
        if self.equipamento and self.equipamento.custo_aquisicao:
            return float(self.equipamento.custo_aquisicao) / 2000
        return 0

    def custo_depreciacao(self):
        if self.equipamento and self.equipamento.data_aquisicao:
            anos = (date.today() - self.equipamento.data_aquisicao).days / 365
            if anos > 0:
                return float(self.equipamento.custo_aquisicao) / anos
        return 0

    def custo_pos_processamento(self, subtotal):
        """Pode ser sobrescrito nas classes filhas se necessário"""
        return subtotal * 0.10  # 10% do subtotal

    def calcular_custo_total(self):
        """Método abstrato, será implementado nas classes filhas"""
        raise NotImplementedError("Essa função deve ser implementada nas classes filhas")

class CalculadoraCustosResina(CalculadoraCustos):
    def __init__(self, equipamento_id, quantidade_resina_g, tempo_horas):
        super().__init__(equipamento_id, tempo_horas)
        self.quantidade_resina = quantidade_resina_g

        # Buscar insumos
        self.alcool = Insumos.objects.filter(nome__icontains='álcool').first()
        self.luvas = Insumos.objects.filter(nome__icontains='luvas').first()
        self.filtro = Insumos.objects.filter(nome__icontains='filtro').first()
        self.energia = Insumos.objects.filter(tipo='energia').first()

        # Buscar a resina
        self.resina = MateriaPrima.objects.filter(tipo='resina').first()

    def custo_resina(self):
        if self.resina and self.resina.preco:
            return self.quantidade_resina * float(self.resina.preco) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        total = 0
        if self.alcool and self.alcool.preco_unitario:
            total += 0.10 * float(self.alcool.preco_unitario)
        if self.luvas and self.luvas.preco_unitario:
            total += 0.05 * float(self.luvas.preco_unitario)
        if self.filtro and self.filtro.preco_unitario:
            total += 0.05 * float(self.filtro.preco_unitario)
        if self.energia and self.energia.preco_unitario:
            potencia_kw = self.equipamento.potencia_watts / 1000
            total += potencia_kw * self.tempo_horas * float(self.energia.preco_unitario)
        return total

    def calcular_custo_total(self):
        subtotal = self.custo_resina() + self.custo_insumos() + \
                   self.custo_manutencao() + self.custo_depreciacao()
        custo_total = subtotal + self.custo_pos_processamento(subtotal)
        return round(custo_total, 2)

class CalculadoraCustosFilamento(CalculadoraCustos):
    def __init__(self, equipamento_id, quantidade_filamento_g, tempo_horas):
        super().__init__(equipamento_id, tempo_horas)
        self.quantidade_filamento = quantidade_filamento_g

        # Buscar insumos específicos
        self.energia = Insumos.objects.filter(tipo='energia').first()
        # Outros insumos específicos do filamento podem ser adicionados

        # Buscar o filamento como matéria-prima
        self.filamento = MateriaPrima.objects.filter(tipo='filamento').first()

    def custo_filamento(self):
        if self.filamento and self.filamento.preco:
            return self.quantidade_filamento * float(self.filamento.preco) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        total = 0
        if self.energia and self.energia.preco_unitario:
            potencia_kw = self.equipamento.potencia_watts / 1000
            total += potencia_kw * self.tempo_horas * float(self.energia.preco_unitario)
        return total

    def calcular_custo_total(self):
        subtotal = self.custo_filamento() + self.custo_insumos() + \
                   self.custo_manutencao() + self.custo_depreciacao()
        custo_total = subtotal + self.custo_pos_processamento(subtotal)
        return round(custo_total, 2)


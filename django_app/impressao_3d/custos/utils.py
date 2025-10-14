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
        """Calcula a depreciação anual e converte para custo por hora"""
        eq = self.equipamento
        if eq.valor_residual == 0 or eq.vida_util_anos <= 0:
            return 0
        
        # vida útil total em horas (anos -> horas)
        vida_util_horas = eq.vida_util_anos * 365 * 24

        # depreciação por hora de uso
        custo_depreciacao_total = (eq.custo_aquisicao - eq.valor_residual)
        custo_depreciacao_hora = custo_depreciacao_total / vida_util_horas

        # Depreciação proporcional ao tempo de uso
        depreciacao_uso = custo_depreciacao_hora * self.tempo_horas
        return round(depreciacao_uso, 2)

    
    def custo_energia(self):
        energia = Insumos.objects.filter(tipo='energia').first()
        if energia and energia.preco_unitario:
            potencia_kw = self.equipamento.potencia_watts / 1000
            return potencia_kw * self.tempo_horas * float(energia.preco_unitario)
        return 0
       
    def custo_pos_processamento(self, subtotal):
        """Pode ser sobrescrito nas classes filhas se necessário"""
        return subtotal * 0.10  # 10% do subtotal

    def calcular_custo_total(self):
        """Método abstrato, será implementado nas classes filhas"""
        raise NotImplementedError("Essa função deve ser implementada nas classes filhas")
    
    def detalhar_custos(self):
        """Método abstrato, será implementado nas classes filhas"""
        raise NotImplementedError("Essa função deve ser implementada nas classes filhas")

class CalculadoraCustosResina(CalculadoraCustos):
    def __init__(self, equipamento_id, quantidade_resina_g, tempo_horas, taxa_perda=0.0):
        super().__init__(equipamento_id, tempo_horas)
        self.quantidade_resina = quantidade_resina_g
        self.taxa_perda = taxa_perda/100  # Convertendo porcentagem para decimal

        # Buscar insumos
        self.alcool = Insumos.objects.filter(nome__icontains='álcool').first()
        self.luvas = Insumos.objects.filter(nome__icontains='luvas').first()
        self.filtro = Insumos.objects.filter(nome__icontains='filtro').first()
        self.energia = Insumos.objects.filter(tipo='energia').first()

        # Buscar a resina
        self.resina = MateriaPrima.objects.filter(tipo='resina').first()

    def custo_resina(self):
        if self.resina and self.resina.preco_unitario:
            return self.quantidade_resina * float(self.resina.preco_unitario) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        total = 0
        if self.alcool and self.alcool.preco_unitario:
            total += 0.10 * float(self.alcool.preco_unitario)
        if self.luvas and self.luvas.preco_unitario:
            total += 0.05 * float(self.luvas.preco_unitario)
        if self.filtro and self.filtro.preco_unitario:
            total += 0.05 * float(self.filtro.preco_unitario)

        return total

    def calcular_custo_total(self):
        subtotal = self.custo_resina() + self.custo_insumos() + self.custo_manutencao() + self.custo_depreciacao() + \
            self.custo_energia()

        custo_total = subtotal + self.custo_pos_processamento(subtotal) + (self.custo_resina() * self.taxa_perda)
        return round(custo_total, 2)
    
    def detalhar_custos(self):
        detalhes = {
            "custo_materia": round(self.custo_resina(), 2),
            "custo_insumos": round(self.custo_insumos(), 2),
            "custo_manutencao": round(self.custo_manutencao(), 2),
            "custo_depreciacao": round(self.custo_depreciacao(), 2),
            "custo_energia": round(self.custo_energia(), 2),
            "depreciacao": round(self.custo_depreciacao(), 2),
            'custo_perda': round(self.custo_resina() * self.taxa_perda, 2),
        }
        subtotal = sum(detalhes.values())
        detalhes["subtotal"] = round(subtotal, 2)
        detalhes["custo_pos_processamento"] = round(self.custo_pos_processamento(subtotal), 2)
        detalhes["custo_total"] = round(self.calcular_custo_total(), 2)
        return detalhes

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
        if self.filamento and self.filamento.preco_unitario:
            return self.quantidade_filamento * float(self.filamento.preco_unitario) / 1000  # Convertendo g para kg
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
    
    def detalhar_custos(self):
        detalhes = {
            "custo_filamento": round(self.custo_filamento(), 2),
            "custo_insumos": round(self.custo_insumos(), 2),
            "custo_manutencao": round(self.custo_manutencao(), 2),
            "custo_depreciacao": round(self.custo_depreciacao(), 2),
        }
        subtotal = sum(detalhes.values())
        detalhes["subtotal"] = round(subtotal, 2)
        detalhes["custo_pos_processamento"] = round(self.custo_pos_processamento(subtotal), 2)
        detalhes["custo_total"] = round(self.calcular_custo_total(), 2)
        return detalhes

from datetime import date
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima, Insumos

class CalculadoraCustos:
    def __init__(self, equipamento_id, tempo_horas):
        self.equipamento = Equipamento.objects.get(id=equipamento_id)
        self.tempo_horas = tempo_horas

    def custo_manutencao(self):
        """Calcula o custo de manutenção proporcional ao tempo de impressão"""
        if self.equipamento and self.equipamento.custo_aquisicao:
            hora_maquina = self.equipamento.custo_aquisicao / 2000
            return hora_maquina * self.tempo_horas
        return 0

    def custo_depreciacao(self):
        """Calcula a depreciação proporcional ao tempo de impressão considerando tempo restante"""
        eq = self.equipamento
        if not eq or eq.vida_util_anos <=0 or eq.valor_residual <=0:
            return 0
        
        # Data de fim da vida útil
        fim_vida_util = eq.data_aquisicao.replace(year=eq.data_aquisicao.year + eq.vida_util_anos) # type: ignore
        hoje = date.today()

        # Tempo restante em dias
        dias_restantes = (fim_vida_util - hoje).days
        if dias_restantes <= 0:
            return 0
        
        # Valor a depreciarpor hora restante
        valor_a_depreciar = max(eq.custo_aquisicao - eq.valor_residual, 0)
        
        if valor_a_depreciar == 0:
            return 0

        horas_restantes = dias_restantes * 24
        depreciacao_hora = valor_a_depreciar / horas_restantes

        # Depreciação proporcional ao tempo de impressão
        custo = depreciacao_hora * self.tempo_horas
        # print(f'Depreciação: {custo}')
        return round(custo,2)

    
    def custo_energia(self):
        energia = Insumos.objects.filter(categoria='energia').first()
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

        # Buscar a resina
        self.resina = MateriaPrima.objects.filter(tipo='resina').first()

        # Buscar insumos relacionados à resina
        self.insumos_resina = Insumos.objects.filter(tipo__in=['resina','geral'])

    def custo_resina(self):
        if self.resina and self.resina.preco_unitario:
            return self.quantidade_resina * float(self.resina.preco_unitario) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        total = 0
        for insumo in self.insumos_resina:
            if insumo.preco_unitario:
                total +=(float(insumo.preco_unitario * (insumo.peso_no_calculo)))
        return total

    def calcular_custo_total(self):
        subtotal = self.custo_resina() + self.custo_insumos() + self.custo_manutencao() + self.custo_depreciacao() + \
            self.custo_energia()

        custo_total = subtotal + self.custo_pos_processamento(subtotal) + (self.custo_resina() * self.taxa_perda)
        return round(custo_total, 2)
    
    def detalhar_custos(self):

        custo_materia = round(self.custo_resina(), 2)
        custo_insumos = round(self.custo_insumos(), 2)
        custo_manutencao = round(self.custo_manutencao(), 2)
        custo_depreciacao = round(self.custo_depreciacao(), 2)
        custo_energia = round(self.custo_energia(), 2)
        custo_perda = round(self.custo_resina() * self.taxa_perda, 2)

        # Subtotal sem custo_perda - igual ao usado em calcular_custo_total()
        subtotal = round(custo_materia + custo_insumos + custo_manutencao + custo_depreciacao + custo_energia, 2)
        custo_pos_processamento = round(self.custo_pos_processamento(subtotal), 2)
        custo_total = round(subtotal + custo_pos_processamento + custo_perda, 2)

    
        return {
            "custo_resina": custo_materia,
            "custo_insumos": custo_insumos,
            "custo_manutencao": custo_manutencao,
            "custo_depreciacao": custo_depreciacao,
            "custo_energia": custo_energia,
            "custo_perda": custo_perda,
            "subtotal": subtotal,
            "custo_pos_processamento": custo_pos_processamento,
            "custo_total": custo_total
        }

class CalculadoraCustosFilamento(CalculadoraCustos):
    def __init__(self, equipamento_id, quantidade_filamento_g, tempo_horas):
        super().__init__(equipamento_id, tempo_horas)
        
        
        self.quantidade_filamento = quantidade_filamento_g

        # Buscar insumos específicos
        # Nota: energia já é tratada pela classe base via custo_energia()
        # Outros insumos específicos do filamento podem ser adicionados

        # Buscar o filamento como matéria-prima
        self.filamento = MateriaPrima.objects.filter(tipo='filamento').first()

    def custo_filamento(self):
        if self.filamento and self.filamento.preco_unitario:
            return self.quantidade_filamento * float(self.filamento.preco_unitario) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        # Exemplo: se houver insumos específicos para filamento, eles podem ser calculados aqui
        # Por enquanto, vamos assumir que não há insumos adicionais além da energia, que é tratada na classe base
        return 0    

    def calcular_custo_total(self):
        subtotal = (self.custo_filamento()
                    + self.custo_energia()
                    + self.custo_insumos() 
                    + self.custo_manutencao() 
                    + self.custo_depreciacao()
                    )
        
        custo_total = subtotal + self.custo_pos_processamento(subtotal)
        return round(custo_total, 2)
    
    def detalhar_custos(self):
        custo_filamento = round(self.custo_filamento(), 2)
        custo_energia = round(self.custo_energia(), 2)
        custo_manutencao = round(self.custo_manutencao(), 2)
        custo_depreciacao = round(self.custo_depreciacao(), 2)

        subtotal = round(custo_filamento + custo_energia + custo_manutencao + custo_depreciacao, 2)
        custo_pos_processamento = round(self.custo_pos_processamento(subtotal), 2)
        custo_total = round(subtotal + custo_pos_processamento, 2)

        return {
            "custo_filamento": custo_filamento,
            "custo_energia": custo_energia,
            "custo_manutencao": custo_manutencao,
            "custo_depreciacao": custo_depreciacao,
            "subtotal": subtotal,
            "custo_pos_processamento": custo_pos_processamento,
            "custo_total": custo_total
        }
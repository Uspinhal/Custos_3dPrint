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
    def __init__(self, equipamento_id, mesas, taxa_perda=0.0, materia_prima_id=None):
        # mesas = [{'quantidade_g': 100, 'tempo_horas': 2.5}, ...]
        tempo_total = sum(m['tempo_horas'] for m in mesas)
        super().__init__(equipamento_id, tempo_total)

        self.mesas = mesas
        self.num_mesas = len(mesas)
        quantidade_total = sum(m['quantidade_g'] for m in mesas)
        self.quantidade_resina = quantidade_total * 1.15
        self.taxa_perda = float(taxa_perda) / 100

        if materia_prima_id:
            self.resina = MateriaPrima.objects.filter(id=materia_prima_id, tipo='resina').first()
        else:
            self.resina = MateriaPrima.objects.filter(tipo='resina').first()

        self.insumos_resina = Insumos.objects.filter(tipo__in=['resina', 'geral'])

    def custo_resina(self):
        if self.resina and self.resina.preco_unitario:
            return self.quantidade_resina * float(self.resina.preco_unitario) / 1000
        return 0

    def custo_insumos(self):
        total = 0
        for insumo in self.insumos_resina:
            if insumo.preco_unitario:
                total += float(insumo.preco_unitario * insumo.peso_no_calculo)
        return total * self.num_mesas  # insumos por rodada × nº de mesas

    def calcular_custo_total(self):
        subtotal = (self.custo_resina() + self.custo_insumos() + self.custo_manutencao()
                    + self.custo_depreciacao() + self.custo_energia())
        custo_total = subtotal + self.custo_pos_processamento(subtotal) + (self.custo_resina() * self.taxa_perda)
        return round(custo_total, 2)

    def detalhar_custos(self):
        custo_materia = round(self.custo_resina(), 2)
        custo_insumos = round(self.custo_insumos(), 2)
        custo_manutencao = round(self.custo_manutencao(), 2)
        custo_depreciacao = round(self.custo_depreciacao(), 2)
        custo_energia = round(self.custo_energia(), 2)
        custo_perda = round(self.custo_resina() * self.taxa_perda, 2)

        subtotal_bruto = (self.custo_resina() + self.custo_insumos() + self.custo_manutencao()
                        + self.custo_depreciacao() + self.custo_energia())
        custo_pos_processamento = round(self.custo_pos_processamento(subtotal_bruto), 2)
        subtotal = round(subtotal_bruto, 2)
        custo_total = self.calcular_custo_total()

        return {
            "tipo": "resina",
            "num_mesas": self.num_mesas,
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
    def __init__(self, equipamento_id, mesas, taxa_perda=0.0, materia_prima_id=None):
        # mesas = [{'quantidade_g': 50, 'tempo_horas': 2.5}, {'quantidade_g': 30, 'tempo_horas': 1.5}]
        tempo_total = sum(m['tempo_horas'] for m in mesas)
        super().__init__(equipamento_id, tempo_total)

        self.mesas = mesas
        self.num_mesas = len(mesas)
        self.quantidade_filamento = sum(m['quantidade_g'] for m in mesas)       
        # Nota: energia já é tratada pela classe base via custo_energia()
        self.insumos_filamento = Insumos.objects.filter(tipo__in=['filamento','geral'])
        self.taxa_perda = float(taxa_perda) / 100
        
        # Buscar o filamento como matéria-prima
        if materia_prima_id:
            self.filamento = MateriaPrima.objects.filter(id=materia_prima_id, tipo='filamento').first()
        else:
            self.filamento = MateriaPrima.objects.filter(tipo='filamento').first()

    def custo_manutencao(self):
        """Calcula o custo de manutenção proporcional ao tempo de impressão"""
        if self.equipamento and self.equipamento.custo_aquisicao:
            #hora_maquina = self.equipamento.custo_aquisicao / 10000
            return self.tempo_horas * 0.3

        return 0

    def custo_filamento(self):
        if self.filamento and self.filamento.preco_unitario:
            return self.quantidade_filamento * float(self.filamento.preco_unitario) / 1000  # Convertendo g para kg
        return 0

    def custo_insumos(self):
        total = 0
        for insumo in self.insumos_filamento:
            if insumo.preco_unitario:
                total +=(float(insumo.preco_unitario * (insumo.peso_no_calculo)))
        return total    

    def calcular_custo_total(self):
        subtotal = (self.custo_filamento()
                    + self.custo_energia()
                    + self.custo_insumos() 
                    + self.custo_manutencao() 
                    + self.custo_depreciacao()
                    )
        
        custo_total = subtotal + self.custo_pos_processamento(subtotal) + (self.custo_filamento() * self.taxa_perda)
        return round(custo_total, 2)
    
    def detalhar_custos(self):
        # Valores individuais arredondados APENAS para exibição
        custo_filamento = round(self.custo_filamento(), 2)
        custo_energia = round(self.custo_energia(), 2)
        custo_manutencao = round(self.custo_manutencao(), 2)
        custo_depreciacao = round(self.custo_depreciacao(), 2)
        custo_insumos = round(self.custo_insumos(), 2)
        custo_perda = round(self.custo_filamento() * self.taxa_perda, 2)

        # Subtotal e total usando valores BRUTOS (igual ao calcular_custo_total)
        subtotal_bruto = (self.custo_filamento() + self.custo_energia()
                        + self.custo_manutencao() + self.custo_depreciacao()
                        + self.custo_insumos())
        custo_pos_processamento = round(self.custo_pos_processamento(subtotal_bruto), 2)
        subtotal = round(subtotal_bruto, 2)
        custo_total = self.calcular_custo_total()

        return {
            "tipo": "filamento",
            "custo_filamento": custo_filamento,
            "custo_energia": custo_energia,
            "custo_perda": custo_perda,
            "custo_manutencao": custo_manutencao,
            "custo_depreciacao": custo_depreciacao,
            "custo_insumos": custo_insumos,
            "subtotal": subtotal,
            "custo_pos_processamento": custo_pos_processamento,
            "custo_total": custo_total
        }
from django.test import TestCase
from custos.utils import CalculadoraCustosResina, CalculadoraCustosFilamento
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima, Insumos

# Create your tests here.
class CalculadoraCustosTest(TestCase):
    def setUp(self):
        # Criar dados de teste no banco
        self.equipamento = Equipamento.objects.create(
            modelo="Impressora Teste",
            potencia_watts=100,
            custo_aquisicao=2,
            data_aquisicao="2022-01-01"
        )

        self.resina = MateriaPrima.objects.create(
            nome="Resina Teste",
            tipo="resina",
            preco=1.0,
            quantidade=100,
            
        )

        self.energia = Insumos.objects.create(
            nome="Energia",
            tipo="energia",
            quantidade=10,
            preco_unitario=0.8
        )

        self.alcool = Insumos.objects.create(
            nome="Álcool",
            tipo="consumivel",
            quantidade=5,
            preco_unitario=10
        )

    def test_custo_resina(self):
        calc = CalculadoraCustosResina(self.equipamento.id, 50, 3) #type: ignore
        custo_total = calc.calcular_custo_total()
        self.assertGreater(custo_total, 0)
        print("Custo total resina (teste):", custo_total)

    def test_custo_filamento(self):
        # Criar filamento
        filamento = MateriaPrima.objects.create(
            nome="Filamento Teste",
            tipo="filamento",
            preco=0.5,
            quantidade=1000,
        )
        calc = CalculadoraCustosFilamento(self.equipamento.id, 100, 3) #type: ignore
        custo_total = calc.calcular_custo_total()
        self.assertGreater(custo_total, 0)
        print("Custo total filamento (teste):", custo_total)
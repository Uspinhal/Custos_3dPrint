from datetime import date
from django.test import TestCase
from custos.utils import CalculadoraCustosResina, CalculadoraCustosFilamento
from custos.forms import TempoImpressaoField
from equipamentos.models import Equipamento
from estoque.models import MateriaPrima, Insumos


class CalculadoraCustosTest(TestCase):
    def setUp(self):
        # Usar date() em vez de string evita TypeError no save() do modelo,
        # que chama calcular_valor_residual() antes da conversão automática do Django.
        self.equipamento = Equipamento.objects.create(
            nome="Impressora Teste",
            tipo="Resina",
            potencia_watts=100,
            custo_aquisicao=2000,
            vida_util_anos=5,
            data_aquisicao=date(2022, 1, 1),
        )

        # FIX: campo correto é preco_total, não preco
        self.resina = MateriaPrima.objects.create(
            nome="Resina Teste",
            tipo="resina",
            quantidade=1,       # 1 kg
            preco_total=100.0,  # R$ 100/kg
        )

        self.energia = Insumos.objects.create(
            nome="Energia Elétrica",
            tipo="geral",
            categoria="energia",
            quantidade=1,
            preco_total=0.80,   # R$ 0,80/kWh
        )

        self.alcool = Insumos.objects.create(
            nome="Álcool Isopropílico",
            tipo="resina",
            categoria="consumivel",
            quantidade=1,
            preco_total=20.0,
            peso_no_calculo=0.5,
        )

    def test_custo_resina_maior_que_zero(self):
        calc = CalculadoraCustosResina(
            equipamento_id=self.equipamento.id,  # type: ignore
            quantidade_resina_g=50,
            tempo_horas=3,
            taxa_perda=5,
        )
        custo_total = calc.calcular_custo_total()
        self.assertGreater(custo_total, 0)
        print("Custo total resina (teste):", custo_total)

    def test_detalhamento_resina_consistente(self):
        """custo_total no breakdown deve bater com calcular_custo_total()."""
        calc = CalculadoraCustosResina(
            equipamento_id=self.equipamento.id,  # type: ignore
            quantidade_resina_g=50,
            tempo_horas=3,
            taxa_perda=5,
        )
        self.assertEqual(calc.calcular_custo_total(), calc.detalhar_custos()["custo_total"])

    def test_custo_filamento_maior_que_zero(self):
        # FIX: campo correto é preco_total, não preco
        MateriaPrima.objects.create(
            nome="Filamento Teste",
            tipo="filamento",
            quantidade=1,       # 1 kg
            preco_total=50.0,   # R$ 50/kg
        )
        calc = CalculadoraCustosFilamento(
            equipamento_id=self.equipamento.id,  # type: ignore
            quantidade_filamento_g=100,
            tempo_horas=3,
        )
        custo_total = calc.calcular_custo_total()
        self.assertGreater(custo_total, 0)
        print("Custo total filamento (teste):", custo_total)

    def test_detalhamento_filamento_consistente(self):
        """custo_total no breakdown deve bater com calcular_custo_total()."""
        MateriaPrima.objects.create(
            nome="Filamento Teste",
            tipo="filamento",
            quantidade=1,
            preco_total=50.0,
        )
        calc = CalculadoraCustosFilamento(
            equipamento_id=self.equipamento.id,  # type: ignore
            quantidade_filamento_g=100,
            tempo_horas=3,
        )
        self.assertEqual(calc.calcular_custo_total(), calc.detalhar_custos()["custo_total"])


class TempoImpressaoFieldTest(TestCase):
    def setUp(self):
        self.field = TempoImpressaoField(required=False)

    def _conv(self, valor) -> float:
        result = self.field.to_python(valor)
        assert result is not None, f"Conversão retornou None para '{valor}'"
        return result

    def test_formato_hhmm(self):
        self.assertAlmostEqual(self._conv("2:30"), 2.5)
    
    def test_formato_com_zero(self):
        self.assertAlmostEqual(self._conv("1:05"), 1 + 5 / 60)
 
    def test_so_minutos(self):
        self.assertAlmostEqual(self._conv("0:45"), 0.75)
 
    def test_formato_decimal(self):
        self.assertAlmostEqual(self._conv("2.5"), 2.5)
 
    def test_formato_decimal_virgula(self):
        self.assertAlmostEqual(self._conv("1,5"), 1.5)
 
    def test_formato_com_h(self):
        self.assertAlmostEqual(self._conv("2h30"), 2.5)
 
    def test_minutos_invalidos(self):
        with self.assertRaises(Exception):
            self._conv("2:60")
 
    def test_formato_invalido(self):
        with self.assertRaises(Exception):
            self._conv("duas horas")
   
 
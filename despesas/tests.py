from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Categoria, Despesa, Deposito
from .forms import RegistroForm, LoginForm
from datetime import date 
from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium import webdriver
from django.core.exceptions import ValidationError
# --------- TESTES DE MODELOS ---------

class CategoriaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_categoria_creation(self):
        categoria = Categoria.objects.create(
            nome='Alimentação',
            descricao='Gastos com comida',
            usuario=self.user
        )
        self.assertEqual(str(categoria), 'Alimentação')
        self.assertEqual(categoria.descricao, 'Gastos com comida')
        self.assertEqual(categoria.usuario, self.user)

    def test_categoria_descricao_blank(self):
        categoria = Categoria.objects.create(
            nome='Transporte',
            descricao='',
            usuario=self.user
        )
        self.assertEqual(categoria.descricao, '')


class DespesaModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.categoria = Categoria.objects.create(nome='Saúde', usuario=self.user)

    def test_despesa_creation(self):
        despesa = Despesa.objects.create(
            nome='Consulta médica',
            descricao='Consulta de rotina',
            data='2024-10-15',
            categoria=self.categoria,
            valor=250.00,
            usuario=self.user
        )
        self.assertEqual(str(despesa), 'Consulta médica')
        self.assertEqual(despesa.valor, 250.00)
        self.assertEqual(despesa.categoria, self.categoria)
        self.assertEqual(despesa.usuario, self.user)

    def test_despesa_valor_negativo(self):
        despesa = Despesa(valor=-50)  # Valor negativo
        with self.assertRaises(ValidationError):
            despesa.clean()  # Deve levantar ValidationError

    def test_despesa_data_futura(self):
        data_futura = date.today().replace(year=date.today().year + 1)
        despesa = Despesa.objects.create(
            nome='Consulta médica',
            descricao='Consulta de rotina',
            data=data_futura,
            categoria=self.categoria,
            valor=250.00,
            usuario=self.user
        )
        self.assertEqual(despesa.data, data_futura)


class DepositoModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.categoria = Categoria.objects.create(nome='Investimentos', usuario=self.user)

    def test_deposito_creation(self):
        deposito = Deposito.objects.create(
            usuario=self.user,
            categoria=self.categoria,
            valor=1000.00,
            data='2024-10-15',
            descricao='Depósito em poupança'
        )
        self.assertEqual(str(deposito), 'Depósito em poupança - 1000.00')
        self.assertEqual(deposito.valor, 1000.00)
        self.assertEqual(deposito.categoria, self.categoria)
        self.assertEqual(deposito.usuario, self.user)

    def test_deposito_valor_negativo(self):
        deposito = Deposito(valor=-100)  # Valor negativo
        with self.assertRaises(ValidationError):
            deposito.clean()  # Deve levantar ValidationError


# --------- TESTES DE VIEWS ---------

class AuthViewsTest(TestCase):
    def test_registrar_view(self):
        response = self.client.get(reverse('registrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas/registrar.html')

    def test_login_view(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'despesas/login.html')

    def test_login_post(self):
        user = User.objects.create_user(username='testuser', password='12345')
        login_data = {'username': 'testuser', 'password': '12345'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertRedirects(response, reverse('lista_despesas'))

    def test_login_incorreto(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'senhaerrada'})
        self.assertEqual(response.status_code, 200)  

    def test_logout_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertFalse(response.wsgi_request.user.is_authenticated)


# --------- TESTES DE FORMULÁRIOS ---------

class RegistroFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com', 
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        }
        form = RegistroForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            'username': 'testuser',
            'password1': 'strongpassword123',
            'password2': 'differentpassword123',
        }
        form = RegistroForm(data=form_data)
        self.assertFalse(form.is_valid())


class LoginFormTest(TestCase):
    def test_valid_login(self):
        user = User.objects.create_user(username='testuser', password='12345')
        form_data = {'username': 'testuser', 'password': '12345'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_login(self):
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())


# --------- TESTES DE INTEGRAÇÃO ---------

class AuthIntegrationTestCase(TestCase):
    def test_registro_e_login(self):
        response = self.client.post(reverse('registrar'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
        })
        self.assertEqual(response.status_code, 302)  

        login_data = {'username': 'testuser', 'password': 'strongpassword123'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertRedirects(response, reverse('lista_despesas'))  

    def test_login_com_usuario_inexistente(self):
        login_data = {'username': 'usuario_inexistente', 'password': 'senhaerrada'}
        response = self.client.post(reverse('login'), data=login_data)
        self.assertEqual(response.status_code, 200) 


class CategoriaIntegrationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_categoria_criacao_e_listagem(self):
        response = self.client.post(reverse('gerenciar_categorias'), {'nome': 'Transporte'})
        self.assertEqual(response.status_code, 302)  

        response = self.client.get(reverse('gerenciar_categorias'))
        self.assertContains(response, 'Transporte')


# --------- TESTES SELENIUM ---------

class SistemaAuthTestCase(LiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def tearDown(self):
        self.browser.quit()

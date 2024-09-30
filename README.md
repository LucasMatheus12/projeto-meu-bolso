PASSOS PARA RODAR  O PROJETO:
1. Realizar o git clone
      git clone https://github.com/LucasMatheus12/projeto-meu-bolso
2. criar uma virtual env
COMANDO LINUX: sudo apt install python3-virtualenv
               virtualenv -p python .venv_back
               . .venv_back/bin/activate
COMANDO WINDOWS: 
              python -m venv .venv_back
              .\.venv_back\Scripts\activate
3. instalar as dependências
               pip install -r equipaments-dev.txt
4. Criar arquivo chamado .env na raiz da pasta back-end com as configurações:
              SECRET_KEY='b4c-6kjjtl9s6@o5(5b+)t5v9utaqvinqzr)3)_os_bk@5qxws
              DEBUG=True
              EMAIL_HOST_USER=""
              EMAIL_HOST_PASSWORD=""
5. Rode o migrate e crie um super usuário
              python manage.py migrate
              python manage.py createsuperuser
No superusuário você adicionar o seu username, um e-mail e uma senha
6. Rode o runserver
              python manage.py runserver
7. Acesse Localhost:8000/admin e faça seu login



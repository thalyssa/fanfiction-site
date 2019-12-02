import os
import json

class View:
    def __init__(self, state):
        self.state = state

    def prompt(self):
        print('Proto shit, don\'t use.')
        return ''

    def run(self, option: str):
        print(f'Opção: {option}')


class InitView(View):
    def prompt(self):
        print("Bem vindo! Escolha uma opção:")
        print("1 - Criar perfil")
        print("2 - Login")
        print("3 - Encerrar")

        option = input("\n")
        return option

    def run(self, option: str):
        if option == '1':
            self.createUser()
        elif option == '2':
            self.login()
        elif option == '3':
            self.state.running = False
        else:
            print('Opção inválida')

    def login(self):
        username = input('Digite o usuário:')
        password = input('Digite a senha:')

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        if username in users_data['users']:
            if users_data['users'][username]['pass'] == password:
                print('Usuário encontrado e senha correta')
                self.state.username = username
                self.state.userdata = users_data['users'][username]
                v = LoggedView(self.state)
                self.state.view = v
            else:
                print('Senha incorreta')
        else:
            print('Usuário não encontrado')

    def createUser(self):
        username = input("Digite um nome de usuário (Deve ser único e sem caracteres espciais): ")
        email = input("Digite um endereço de e-mail: ")
        password = input("Digite uma senha: ")

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        if not username in users_data['users']:
            users_data['users'][username] = {'email': email, 'pass': password}
            with open(self.state.users_json_path, 'w') as file:
                json.dump(users_data, file)

class LoggedView(View):
    def prompt(self):
        print(f"Olá, {self.state.username}!")
        print(f"E-mail: {self.state.userdata['email']}\n")
        print("1 - Listar Minhas Estórias")
        print("2 - Listar estórias favoritas")
        print("3 - Listar autores favoritos")
        print("4 - Pesquisar estórias")
        print("5 - Alterar Dados Pessoais")
        print("6 - Logout")
        print("7 - Excluir Minha Conta")

        option = input('\n')
        return option


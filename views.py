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
            pass
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
            if users_data['users'][username]['senha'] == password:
                print('Usuário encontrado e senha correta')
            else:
                print('Senha incorreta')
        else:
            print('Usuário não encontrado')




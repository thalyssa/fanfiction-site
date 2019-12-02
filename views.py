import os
import json
import shutil


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

            user_path = os.path.join(self.state.users_data_path, username)
            if os.path.isdir(user_path):
                shutil.rmtree(user_path)
            os.mkdir(user_path)
        else:
            print('Usuário já existe!\n')

class LoggedView(View):
    def prompt(self):
        print(f"Olá, {self.state.username}!")
        print(f"E-mail: {self.state.userdata['email']}\n")

        print("0 - Criar história")
        print("1 - Listar Minhas Estórias")
        print("2 - Listar estórias favoritas")
        print("3 - Listar autores favoritos")
        print("4 - Pesquisar estórias")
        print("5 - Alterar Dados Pessoais")
        print("6 - Logout")
        print("7 - Excluir Minha Conta")

        option = input('\n')
        return option

    def run(self, option):
        if option == '0':
            v = CreateStoryView(self.state)
            self.state.view = v
        elif option == '1':
            pass
        elif option == '2':
            pass
        elif option == '3':
            pass
        elif option == '4':
            pass
        elif option == '5':
            pass
        elif option == '6':
            self.state.username = None
            self.state.userdata = None
            v = InitView(self.state)
            self.state.view = v
        elif option == '7':
            pass
        else:
            print('Opção inválida')

class CreateStoryView(View):
    def prompt(self):
        print('--Criar história--')
        title = input('Título: ')
        rating = input('Classificação: ')
        genre = input('Gênero: ')
        category = input('Categoria: ')
        synopsis = input('Sinopse: ')
        author = self.state.username
        is_finished = False

        story_data = {'title' : title, 'rating' : rating, 'genre' : genre, 'category' : category, 'synopsis' : synopsis, 'author' : author, 'is_finished' : is_finished}

        stories_data_path = os.path.join(self.state.users_data_path, self.state.username, title)
        story_file_name = os.path.join(stories_data_path, 'story_data.json')

        if not os.path.isdir(stories_data_path):
            os.mkdir(stories_data_path)

        with open(story_file_name, 'w') as file:
            json.dump(story_data, file)

    def run(self, option):
        pass

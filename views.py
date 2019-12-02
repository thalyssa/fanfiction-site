import os
import json
import shutil
import subprocess


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

        story_data_path = os.path.join(self.state.users_data_path, self.state.username, title.lower())
        if os.path.isdir(story_data_path):
            print('Estória já existente!')
            return

        rating = input('Classificação: ')
        genre = input('Gênero: ')
        category = input('Categoria: ')
        synopsis = input('Sinopse: ')
        author = self.state.username
        is_finished = False

        story_data = {'title' : title, 'rating' : rating, 'genre' : genre, 'category' : category, 'synopsis' : synopsis, 'author' : author, 'chapters': [], 'is_finished' : is_finished}

        story_file_name = os.path.join(story_data_path, 'story_data.json')

        if not os.path.isdir(story_data_path):
            os.mkdir(story_data_path)

        with open(story_file_name, 'w') as file:
            json.dump(story_data, file)

        self.state.current_story = story_data_path

        v = WorkingStoryView(self.state)
        self.state.view = v




    def run(self, option):
        pass

class WorkingStoryView(View):

    story_data: dict
    story_data_path: str

    def run(self, option):
        if option == '1':
            self.create_new_chapter()
        elif option == '2':
            pass
        elif option == '3':
            pass
        elif option == '4':
            pass
        elif option == '5':
            pass
        else:
            print('Opção inválida')

    def prompt(self):
        self.story_data_path = os.path.join(self.state.current_story, 'story_data.json')
        with open(self.story_data_path, 'r') as file:
            self.story_data = json.load(file)
        print(f'Visualizando: {self.story_data["title"]}')

        print('--- Capítulos ---')
        chapters_count = len(self.story_data['chapters'])

        for i in range(0, chapters_count):
            print(f' c{i} - {self.story_data["chapters"][i]}')

        print()
        print('1 - Novo capítulo')
        print('2 - Editar capítulo')
        print('3 - Excluir capítulo')
        print('4 - Editar dados da estória')
        print('5 - Voltar')

        option = input('\n')
        return option

    def create_new_chapter(self):

        chapter_name = input('Nome do capítulo: ')

        self.story_data['chapters'].append(chapter_name)

        with open(self.story_data_path, 'w') as file:
            json.dump(self.story_data, file)

        chapter_index = len(self.story_data['chapters']) - 1
        chapter_file_path = os.path.join(self.state.current_story, f'{chapter_index}.txt')

        subprocess.run(['nano', chapter_file_path])

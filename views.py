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

    def __init__(self, state):
        self.state = state
        with open(self.state.users_json_path, 'r') as file:
            self.state.admins_list = (json.load(file))['admins']

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

            user_json_path = os.path.join(self.state.users_data_path, username, 'user_data.json')

            with open(user_json_path, 'r') as file:
                user_data = json.load(file)

            if user_data['pass'] == password:
                print('Usuário encontrado e senha correta')
                self.state.username = username
                self.state.userdata = user_data
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

            users_data['users'].append(username)

            with open(self.state.users_json_path, 'w') as file:
                json.dump(users_data, file)

            user_path = os.path.join(self.state.users_data_path, username)

            if os.path.isdir(user_path):
                shutil.rmtree(user_path)

            os.mkdir(user_path)

            user_index = len(users_data['users']) - 1
            user_data = {'index': user_index, 'email': email, 'pass': password, 'stories': []}

            user_json_path = os.path.join(user_path, 'user_data.json')

            with open(user_json_path, 'w') as file:
                json.dump(user_data, file)

        else:
            print('Usuário já existe!\n')


class LoggedView(View):

    def __init__(self, state):
        self.state = state
        self.users_data_json_path = os.path.join(self.state.users_data_path, self.state.username, 'user_data.json')
        with open(self.users_data_json_path, 'r') as file:
            self.user_data = json.load(file)

    def prompt(self):
        print(f"Olá, {self.state.username}!")
        print(f"E-mail: {self.state.userdata['email']}\n")

        print("0 - Criar história")
        print("1 - Listar Minhas Estórias")
        print("2 - Listar estórias favoritas")
        print("3 - Listar autores favoritos")
        print("4 - Pesquisar estórias")
        print("5 - Alterar Perfil")
        print("6 - Logout")
        print("7 - Excluir Minha Conta")

        if self.state.username in self.state.admin_list:
            print("8 - Painel de administrador")

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
            self.update_profile()
        elif option == '6':
            self.state.username = None
            self.state.userdata = None
            v = InitView(self.state)
            self.state.view = v
        elif option == '7':
            pass
        elif option == '8' and self.state.username in self.state.admin_list:
            v = AdminControlPanelView(self.state)
            self.state.view = v
        else:
            print('Opção inválida')

    def update_profile(self):
        print('Alterando dados pessoais')
        email = input('Novo e-mail: ')
        password = input('Nova senha: ')

        self.user_data['email'] = email
        self.user_data['pass'] = password

        with open(self.users_data_json_path, 'w') as file:
            json.dump(self.user_data, file)

        self.state.userdata = self.user_data


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

        story_data = {'title': title, 'rating': rating, 'genre': genre, 'category': category, 'synopsis': synopsis,
                      'author': author, 'chapters': [], 'is_finished': is_finished}

        story_file_name = os.path.join(story_data_path, 'story_data.json')

        if not os.path.isdir(story_data_path):
            os.mkdir(story_data_path)

        with open(story_file_name, 'w') as file:
            json.dump(story_data, file)

        self.state.current_story = story_data_path

        user_json_path = os.path.join(self.state.users_data_path, self.state.username, 'user_data.json')
        with open(user_json_path, 'r') as file:
            user_data = json.load(file)

        user_data['stories'].append(title.lower())

        with open(user_json_path, 'w') as file:
            json.dump(user_data, file)

        v = WorkingStoryView(self.state)
        self.state.view = v

    def run(self, option):
        pass


class WorkingStoryView(View):
    story_data: dict
    story_data_path: str

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

    def create_new_chapter(self):

        chapter_name = input('Nome do capítulo: ')

        self.story_data['chapters'].append(chapter_name)

        with open(self.story_data_path, 'w') as file:
            json.dump(self.story_data, file)

        chapter_index = len(self.story_data['chapters']) - 1
        chapter_file_path = os.path.join(self.state.current_story, f'{chapter_index}.txt')

        subprocess.run(['nano', chapter_file_path])


class SearchView(View):
    def prompt(self):
        print('Busca de estorias')
        print('1 - Busca por titulo')
        print('2 - Busca por autor')
        print('3 - Voltar')

        option = input('\n')
        return option

    def run(self, option: str):
        if option == '1':
            pass
        elif option == '2':
            self.search_by_author()
        elif option == '3':
            pass
        else:
            print('Opçao invalida')

    def search_by_author(self):
        name = input('Termo de busca: ')

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        results = []

        for username in users_data['users']:
            if name in username:
                results.append(username)

        length = len(results)
        if length < 1:
            print('Nenhum resultado encontrado.')
            return

        for i in range(0, length):
            print(f' {i} - {results[i]}')

        option = input('Escolha um autor para vizualizar as obras: ')

        option = int(option)
        if option < length:
            v = AuthorView(self.state, results[option])
            self.state.view = v


class AuthorView(View):
    def __init__(self, state, author):
        self.state = state
        self.author = author
        self.author_dir_path = os.path.join(self.state.users_data_path, author)
        self.author_json_path = os.path.join(self.state.users_data_path, author, 'user_data.json')
        with open(self.author_json_path, 'r') as file:
            self.author_data = json.load(file)

    def prompt(self):
        print(f'Bem vindo ao perfil de {self.author}')

        length = len(self.author_data['stories'])
        i = 0

        if length < 1:
            print('Nenhuma obra publicada')
        else:
            print('Obras: ')
            for i in range(0, length):
                print(f'{i} - {self.author_data["stories"][i]}')
            print(f'{i} - Voltar')

        option = input('Opcao: ')
        return int(option)

    def run(self, option: str):

        if len(self.author_data['stories']) < 1:
            # TODO: Voltar para view anterior
            pass
        elif option >= len(self.author_data['stories']):
            # TODO: Voltar para view anterior
            pass
        elif option >= 0:
            story_path = os.path.join(self.author_dir_path, self.author_data['stories'][option])
            v = ReadStoryView(self.state, story_path)
            self.state.view = v


class ReadStoryView(View):
    def __init__(self, state, story_path):
        self.state = state
        self.story_path = story_path


class AdminControlPanelView(View):
    def prompt(self):
        print('Painel de Controle da Administração')
        print('1 - Adicionar uma nova categoria')
        print('2 - Remover usuário')

        option = input('Digite sua opção')
        return option

    def run(self, option: str):
        if option == '1':
            pass
        elif option == '2':
            self.remove_user()
        else:
            print('Opção inválida!')

    def remove_user(self):
        name = input('Termo de busca: ')

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        results = []

        for username in users_data['users']:
            if name in username:
                results.append(username)

        length = len(results)
        if length < 1:
            print('Nenhum resultado encontrado.')
            return

        for i in range(0, length):
            print(f' {i} - {results[i]}')

        option = int(input('Escolha o usuário a ser deletado: '))

        self.user_dir_path = os.path.join(self.state.users_data_path, results[option])

        if os.path.isdir(self.user_dir_path):
            shutil.rmtree(self.user_dir_path)

        users_data['users'].remove(results[option])

        with open(self.state.users_json_path, 'w') as file:
            json.dump(users_data, file)

        print('Usuario removido com sucesso')

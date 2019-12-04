import os
import json
import shutil
import subprocess


class View:

    def __init__(self, state):
        self.state = state
        self.reload_user()
        self.reload_admins()

    def reload_user(self):
        if self.state.username is not None:
            user_home = os.path.join(self.state.users_data_path, self.state.username)
            user_json_path = os.path.join(user_home, 'user_data.json')
            with open(user_json_path, 'r') as file:
                user_data = json.load(file)
            self.state.user_home = user_home
            self.state.user_json_path = user_json_path
            self.state.user_data = user_data

    def reload_admins(self):
        with open(self.state.users_json_path, 'r') as file:
            self.state.admins_list = (json.load(file))['admins']

    def prompt(self):
        option = input('Nada acontecerá.')
        return option

    def run(self, option: str):
        print(f'Opção: {option}')

    def back(self):
        if len(self.state.view_stack) > 0:
            self.state.view = self.state.view_stack.pop()

    def switch_view(self, next_view):
        self.state.view_stack.append(self)
        self.state.view = next_view


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
        username = input('Digite o usuário: ')
        password = input('Digite a senha: ')

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        if username in users_data['users']:

            user_json_path = os.path.join(self.state.users_data_path, username, 'user_data.json')

            with open(user_json_path, 'r') as file:
                user_data = json.load(file)

            if user_data['pass'] == password:
                self.state.username = username
                self.state.user_data = user_data
                v = LoggedView(self.state)
                self.switch_view(v)
            else:
                print('Senha incorreta')
        else:
            print('Usuário não encontrado')

    def createUser(self):
        username = input("\nDigite um nome de usuário: ")
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
            user_data = {'index': user_index, 'email': email, 'pass': password, 'stories': [], 'fav_authors': [],
                         'fav_stories': []}

            user_json_path = os.path.join(user_path, 'user_data.json')

            with open(user_json_path, 'w') as file:
                json.dump(user_data, file)

        else:
            print('Usuário já existe!\n')


class LoggedView(View):

    def prompt(self):
        print(f"\nOlá, {self.state.username}!")
        print(f"E-mail: {self.state.user_data['email']}\n\n")

        print("1 - Criar história")
        print("2 - Listar minhas histórias")
        print("3 - Favoritos")
        print("4 - Pesquisar histórias")
        print("5 - Alterar perfil")
        print("6 - Logout")

        if self.state.username in self.state.admin_list:
            print("7 - Painel de administrador")

        option = input('\n\n')
        return option

    def run(self, option):
        if option == '1':
            self.create_story()
        elif option == '2':
            self.list_my_stories()
        elif option == '3':
            v = FavoritesView(self.state)
            self.switch_view(v)
        elif option == '4':
            v = SearchView(self.state)
            self.switch_view(v)
        elif option == '5':
            self.update_profile()
        elif option == '6':
            self.state.username = None
            self.state.user_data = None
            v = InitView(self.state)
            self.switch_view(v)
        elif option == '7' and self.state.username in self.state.admin_list:
            v = AdminControlPanelView(self.state)
            self.switch_view(v)
        else:
            print('Opção inválida')

    def update_profile(self):
        print('\n\nAlterando dados pessoais\n\n')
        email = input('Novo e-mail: ')
        password = input('Nova senha: ')

        self.state.user_data['email'] = email
        self.state.user_data['pass'] = password

        with open(self.state.user_json_path, 'w') as file:
            json.dump(self.state.user_data, file)

        self.state.user_data = self.state.user_data

    def list_my_stories(self):

        stories_list_length = len(self.state.user_data['stories'])
        print()
        for i in range(0, stories_list_length):
            print(f'{i} - {self.state.user_data["stories"][i]}')

        option = input('Escolha uma história\n')
        if option.isnumeric():
            option = int(option)
            current_story_path = os.path.join(self.state.users_data_path, self.state.username,
                                              self.state.user_data['stories'][option])
            self.state.current_story_home = current_story_path

            v = WorkingStoryView(self.state)
            self.switch_view(v)

    def create_story(self):
        print('--Criar história--\n')
        title = input('Título: ')

        story_data_path = os.path.join(self.state.user_home, title.lower())

        if os.path.isdir(story_data_path):
            print('História já existente!')
            return

        rating = input('Classificação: ')
        genre = input('Gênero: ')
        synopsis = input('Sinopse: ')
        author = self.state.username
        is_finished = False

        story_data = {'title': title, 'rating': rating, 'genre': genre, 'synopsis': synopsis,
                      'author': author, 'chapters': [], 'is_finished': is_finished}

        story_file_name = os.path.join(story_data_path, 'story_data.json')

        if not os.path.isdir(story_data_path):
            os.mkdir(story_data_path)

        with open(story_file_name, 'w') as file:
            json.dump(story_data, file)

        self.state.current_story_home = story_data_path

        self.state.user_data['stories'].append(title.lower())

        with open(self.state.user_json_path, 'w') as file:
            json.dump(self.state.user_data, file)


class WorkingStoryView(View):
    story_data: dict
    story_json_path: str

    def __init__(self, state):
        super(WorkingStoryView, self).__init__(state)
        self.story_json_path = os.path.join(self.state.current_story_home, 'story_data.json')
        with open(self.story_json_path, 'r') as file:
            self.story_data = json.load(file)

    def prompt(self):

        print(f'Visualizando: {self.story_data["title"]}')

        print('\n--- Capítulos ---\n')
        chapters_count = len(self.story_data['chapters'])

        for i in range(0, chapters_count):
            print(f' c{i} - {self.story_data["chapters"][i]}')

        print()
        print('1 - Novo capítulo')
        print('2 - Editar capítulo')
        print('3 - Excluir capítulo')
        print('4 - Excluir esta história')
        print('5 - Voltar')

        option = input('\n')
        return option

    def run(self, option):
        if option == '1':
            self.create_new_chapter()
        elif option == '2':
            self.edit_chapter()
        elif option == '3':
            self.remove_chapter()
        elif option == '4':
            self.remove_story()
        elif option == '5':
            self.back()
        else:
            print('Opção inválida')

    def create_new_chapter(self):

        chapter_name = input('\nNome do capítulo: ')

        self.story_data['chapters'].append(chapter_name)

        with open(self.story_json_path, 'w') as file:
            json.dump(self.story_data, file)

        chapter_index = len(self.story_data['chapters']) - 1
        chapter_file_path = os.path.join(self.state.current_story_home, f'{chapter_index}.txt')

        if os.name is 'nt':
            subprocess.call(['notepad', chapter_file_path])
        else:
            subprocess.run(['nano', chapter_file_path])

    def remove_chapter(self):

        option = input('\nDigite o índice do capítulo a ser excluído: ')
        option = option.lower()
        option = option.strip('c')
        option = int(option)

        story_json_path = os.path.join(self.state.current_story_home, 'story_data.json')

        with open(story_json_path, 'r') as file:
            current_story_data = json.load(file)

        chapter_list_length = len(current_story_data['chapters'])

        del current_story_data['chapters'][option]
        with open(story_json_path, 'w') as file:
            json.dump(current_story_data, file)

        chapter_name = str(option) + '.txt'
        chapter_file_path = os.path.join(self.state.current_story_home, chapter_name)

        print('Removendo:\n', chapter_file_path)
        os.remove(chapter_file_path)

        for i in range(option + 1, chapter_list_length):
            source_file_path = os.path.join(self.state.current_story_home, str(i) + '.txt')
            dest_file_path = os.path.join(self.state.current_story_home, str(i - 1) + '.txt')
            os.rename(source_file_path, dest_file_path)

        print('Capítulo excluído com sucesso')

        self.story_data = current_story_data

    def remove_story(self):

        option = input(f'\nApagar permanentemente {self.story_data["title"]} ? [s/N]')

        if option.lower() == 's':

            self.state.user_data['stories'].remove(self.story_data['title'].lower())

            with open(self.state.user_json_path, 'w') as file:
                json.dump(self.state.user_data, file)

            shutil.rmtree(self.state.current_story_home)
            self.state.current_story_home = None

            print('História removida com sucesso')

            self.back()

        else:
            return

    def edit_chapter(self):
        chapter_num = input('Índice do capítulo: \n')
        chapter_file_path = os.path.join(self.state.current_story_home, f'{chapter_num}.txt')

        if os.path.isfile(chapter_file_path):
            if os.name is 'nt':
                subprocess.run(['notepad', chapter_file_path])
            else:
                subprocess.run(['nano', chapter_file_path])
        else:
            print('Índice inválido')


class SearchView(View):
    def prompt(self):
        print('\nBusca de histórias\n')
        print('1 - Busca por título')
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
            self.back()
        else:
            print('Opção inválida')

    def search_by_author(self):
        name = input('Termo de busca: ')
        print()

        with open(self.state.users_json_path, 'r') as file:
            users_data = json.load(file)

        results = []

        for author in users_data['users']:
            if name in author:
                results.append(author)

        length = len(results)
        if length < 1:
            print('\nNenhum resultado encontrado.')
            return

        for i in range(0, length):
            print(f' {i} - {results[i]}')

        option = input('\nEscolha um autor para vizualizar as obras: ')

        option = int(option)
        if option < length:
            v = AuthorView(self.state, results[option])
            self.switch_view(v)


class AuthorView(View):
    def __init__(self, state, author):
        super(AuthorView, self).__init__(state)
        self.author = author
        self.author_home = os.path.join(self.state.users_data_path, author)
        self.author_json_path = os.path.join(self.state.users_data_path, author, 'user_data.json')
        with open(self.author_json_path, 'r') as file:
            self.author_data = json.load(file)

    def prompt(self):
        print(f'Bem vindo ao perfil de {self.author}\n')

        length = len(self.author_data['stories'])
        i = 0

        if length < 1:
            print('Nenhuma obra publicada\n')
        else:
            print('\nObras: ')
            for i in range(0, length):
                print(f'{i} - {self.author_data["stories"][i]}')

        print()
        print(f'{length} - Adicionar autor aos favoritos')
        print(f'{length + 1} - Voltar')

        option = input('\nOpção: ')
        return int(option)

    def run(self, option: str):

        if not str(option).isnumeric():
            print('Opção inválida')
            return

        opt = int(option)

        stories_count = len(self.author_data['stories'])

        if stories_count < 1:
            if opt == 0:
                self.add_fav_author()
            else:
                self.back()
        elif opt == stories_count:
            self.add_fav_author()
        elif opt >= stories_count + 1:
            self.back()
        elif opt >= 0:
            story_path = os.path.join(self.author_home, self.author_data['stories'][opt])
            v = ReadStoryView(self.state, story_path)
            self.switch_view(v)

    def add_fav_author(self):

        if self.author in self.state.user_data['fav_authors']:
            print('Autor já favoritado\n')
            return
        else:
            self.state.user_data['fav_authors'].append(self.author)
            with open(self.state.user_json_path, 'w') as file:
                json.dump(self.state.user_data, file)
            print('Autor favoritado!')


class FavoritesView(View):

    def prompt(self):
        print('\n-Favoritos-\n')
        print('1 - Autores favoritos')
        print('2 - Histórias favoritas')
        print('3 - Voltar')

        option = input('\nOpção: ')
        return option

    def run(self, option: str):
        if option == '1':
            self.list_fav_authors()
        elif option == '2':
            self.list_fav_stories()
        elif option == '3':
            self.back()
        else:
            print('Opção inválida')

    def list_fav_authors(self):
        print('-Autores favoritos-\n')

        i: int

        fav_authors_len = len(self.state.user_data['fav_authors'])

        for i in range(0, fav_authors_len):
            print(f'{i} - {self.state.user_data["fav_authors"][i]}')
        print(f'{fav_authors_len} - Voltar')

        option = int(input('\nOpção: '))

        if option < fav_authors_len:
            v = AuthorView(self.state, self.state.user_data["fav_authors"][option])
            self.switch_view(v)
        elif option == fav_authors_len:
            self.back()
        else:
            print('Opção inválida')

    def list_fav_stories(self):
        print('\n-Histórias favoritas-\n')

        i: int

        fav_stories_len = len(self.state.user_data['fav_stories'])

        for i in range(0, fav_stories_len):
            full_path = self.state.user_data['fav_stories'][i]
            broken_path = []
            if os.name is 'nt':
                broken_path = full_path.split('\\')
            else:
                broken_path = full_path.split('/')
            story_name = broken_path[-1]
            print(f'{i} - {story_name}')
        print(f'\n{fav_stories_len} - Voltar')

        option = input('\nOpção: ')

        if option.isnumeric():
            option = int(option)
            if option == fav_stories_len:
                self.back()
            elif (option < 0) and (option > fav_stories_len):
                print('Opção inválida')
            else:
                v = ReadStoryView(self.state, self.state.user_data['fav_stories'][option])
                self.switch_view(v)

        else:
            print('Opção inválida')


class ReadStoryView(View):
    def __init__(self, state, story_path):
        super(ReadStoryView, self).__init__(state)
        self.story_path = story_path
        self.story_json_path = os.path.join(story_path, 'story_data.json')
        with open(self.story_json_path, 'r') as file:
            self.story_data = json.load(file)

    def prompt(self):
        print()
        print(f'Título: {self.story_data["title"]}')
        print(f'Classificação: {self.story_data["rating"]}')
        print(f'Gênero: {self.story_data["genre"]}')
        print(f'Sinopse: {self.story_data["synopsis"]}')
        print(f'Autor: {self.story_data["author"]}')
        print(f'Completo: {self.story_data["is_finished"]}')
        print()

        i = 0
        chapters_count = len(self.story_data['chapters'])

        if chapters_count < 1:
            print('Sem capítulos publicados.')
        else:
            for i in range(0, chapters_count):
                print(f'{i} - {self.story_data["chapters"][i]}')

        print(f'\n{chapters_count} - Voltar')
        print()

        if self.story_path in self.state.user_data['fav_stories']:
            print(f'{chapters_count + 1} - Remover dos favoritos')
        else:
            print(f'{chapters_count + 1} - Adicionar aos favoritos')

        option = input('Opção: ')
        return option

    def run(self, option: str):

        if not option.isnumeric():
            print('Opção inválida')
            return

        opt = int(option)
        chapters_count = len(self.story_data['chapters'])

        if opt == chapters_count:
            self.back()
        elif opt < 0:
            print('Opção inválida')
        elif opt == chapters_count + 1:
            self.add_fav_story()
        else:
            self.display_chapter(opt)

    def add_fav_story(self):
        if self.story_path not in self.state.user_data['fav_stories']:
            self.state.user_data['fav_stories'].append(self.story_path)
            with open(self.state.user_json_path, 'w') as file:
                json.dump(self.state.user_data, file)
            print('História salva em seus favoritos\n')
        else:
            print('História já favoritada\n')

    def display_chapter(self, chap_num):
        text_file_path = os.path.join(self.story_path, f'{chap_num}.txt')
        with open(text_file_path, 'r') as file:
            content = file.read()
        print(f'\nCapítulo {chap_num}:\n\n', content, '\n\n')


class AdminControlPanelView(View):
    def prompt(self):
        print('\nPainel de Controle da Administração\n\n')
        print('1 - Remover usuário')
        print('2 - Voltar\n')

        option = input('Digite sua opção')
        return option

    def run(self, option: str):
        if option == '1':
            self.remove_user()
        elif option == '2':
            self.back()
        else:
            print('Opção inválida!')

    def remove_user(self):
        name = input('\nTermo de busca: ')

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
            print(f'\n{i} - {results[i]}\n')

        option = int(input('\nEscolha o usuário a ser deletado: \n'))

        user_home = os.path.join(self.state.users_data_path, results[option])

        if os.path.isdir(user_home):
            shutil.rmtree(user_home)

        users_data['users'].remove(results[option])

        with open(self.state.users_json_path, 'w') as file:
            json.dump(users_data, file)

        print('Usuário removido com sucesso')

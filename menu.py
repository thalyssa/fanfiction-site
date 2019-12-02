import os
import json


def mainMenu():
    """Menu principal e inicia do programa."""
    print("Bem vindo! Escolha uma opção:")
    print("1 - Criar perfil")
    print("2 - Login")
    print("3 - Encerrar")

    option = input()
    return option


def userMenu():
    """Menu do usuário após efetuar login"""
    print("Olá *usuário(carregar nome aqui)*! Opções:")
    print("TODO: Exibir dados do usuario")
    print("1 - Listar Minhas Estórias")
    print("2 - Listar estórias favoritas")
    print("3 - Listar autores favoritos")
    print("4 - Pesquisar estórias")
    print("5 - Alterar Dados Pessoais")
    print("6 - Logout")
    print("7 - Excluir Minha Conta")

    option = input()
    return option


def storiesMenu():
    """Menu de gerenciamento das historias"""
    print("TODO: Listar estórias, com os índices para selecionar uma estória para interagir.")

    option = input()
    return option


def adminMenu():
    """Menu de administração"""
    print("TODO: Add categorias e gerenciar usuários.")

    option = input()
    return option

#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko, sys

# Funcao ssh_comando: conecta em uma maquina via SSH e executa um comando predeterminado
# seu retorno e o resultado do comando executado
def ssh_comando(maquina, usuario, chave, comando):

    # Definicao de variaveis, passando valores conforme os parametros
    maquina = maquina
    usuario = usuario
    chave = chave
    comando = comando

    try:
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # print("Conectando em " + maquina + " com o usuario " + usuario + " utilizando a chave " + chave + " e executando o comando " + comando + "\n")
        client.connect(maquina, username=usuario, key_filename=chave)
        stdin, stdout, stderr = client.exec_command(comando)
    
        # Pegar a saida padrao e a saida de erro padrao, concatenando-as para a variavel alldata
        alldata = str(stdout.read()) + str(stderr.read())
        print("Debug\n" + alldata)
        return alldata

        # stdout = stdout.readlines()
        # stdout = str(stdout.readlines())
        # return stdout

    except Exception as e:
        return "Deu ruim aqui"

    finally:
        client.close()
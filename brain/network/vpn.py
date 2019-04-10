#!/usr/bin/python
# -*- coding: utf-8 -*-

import paramiko, sys

from network.ssh import *

def vpn(acao, ambiente):
    
    # definicao de variaveis, conforme os parametros passados
    acao = acao
    ambiente = ambiente

    # filtra as acoes possiveis, convertendo-as em comandos
    # chama a funcao "acao" passando o ambiente e o comando como parametros
    if acao == "status":
        comando = "sudo ipsec status" 
    elif acao == "status detalhado":
        comando = "sudo ipsec statusall" 
    elif acao == "stop":
        comando = "sudo echo ipsec down"
    elif acao == "start":
        comando = "sudo echo ipsec up" 
    elif acao == "restart":
        comando = "sudo echo ipsec down ; sudo echo ipsec up"

    # filtra os ambientes possiveis: sqa e prd
    # a chave .pem deve estar no diretorio raiz do modulo brain
    # chama a funcao "ssh_comando" passando os parametros corretos de acordo com o ambiente passado
    if ambiente == "sqa":
        maquina = "10.90.0.13"
        usuario = "dinda-sqa"
        chave = "dinda-sqa.pem"
    elif ambiente == "prd":
        maquina = "10.80.0.15"
        usuario = "dinda-prd"
        chave = "dinda-prd.pem"

    #parametros: hostname|ip, user, chave, comando
    #print "Conectando em " + maquina + " com o usuario " + usuario + " utilizando a chave " + chave + " e executando o comando " + comando + "\n"
    # ssh_comando(maquina, usuario, chave, comando)
    retorno = ssh_comando(maquina, usuario, chave, comando)

    return retorno
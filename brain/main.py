#!/usr/bin/python
# -*- coding: utf-8 -*-

# Importacao de modulos (necessario instalar via pip)
import puka
import json
import datetime

# Funcao de teste para conhecer o conceito de passsagem de parametro para uma funcao
from network.ghost import *

# Chamada ao modulo VPN
from network.vpn import *
# Modulo config (pend: quem usa?)
from config import *
# Modulo time utilizado para informar a hora certa ;)
from time import localtime, gmtime, strftime

def send_queue(queue, payload):
    producer = puka.Client(rabbitmq)
    send_promise = producer.connect()
    producer.wait(send_promise)
    send_promise = producer.queue_declare(queue=queue)
    producer.wait(send_promise)
    # send message to the queue named rabbit
    send_promise = producer.basic_publish(exchange='', routing_key=rabbit_queue_push, body=json.dumps(payload))
    producer.wait(send_promise)
    return True

# dict = {'comando1':listarteste()}

# for key, value in dict.items():
#     if value['msg'] == key:
#         value

def main():

    consumer = puka.Client(rabbitmq)
    receive_promise = consumer.connect()
    consumer.wait(receive_promise)
    receive_promise = consumer.basic_consume(queue=rabbit_queue_read, no_ack=True)

    # Ler eternamente a fila para consumir mensagens novas
    while True:
        received_message = consumer.wait(receive_promise)
        value = json.loads(received_message['body'])
        
        # Teste simples de resposta de mensagem chamando uma funcao "test"
        if value["msg"] == "oi":
            processado = test("ola")
        
        # Ambientes SQA e PRD: para cada decisao, chamar o modulo vpn passando um parametro e um ambiente

        ## Ambiente SQA
        # Verificacao de status
        elif value["msg"] == "vpn status sqa":
            processado = vpn("status", "sqa")
        
        # Verificacao de status detalhado
        elif value["msg"] == "vpn status detalhado sqa" or value["msg"] == "vpn status sqa detalhado":
            processado = vpn("status detalhado", "sqa")
        
        # Solicitacao de stop
        elif value["msg"] == "vpn stop sqa":
            processado = vpn("stop", "sqa")

        # Solicitacao de start
        elif value["msg"] == "vpn start sqa":
            processado = vpn("start", "sqa")

        # Solicitacao de restart
        elif value["msg"] == "vpn restart sqa":
            processado = vpn("restart", "sqa")
        
        ## Ambiente PRD
        # Verificacao de status
        elif value["msg"] == "vpn status prd" or value["msg"] == "vpn status prod":
            processado = vpn("status", "prd")
        
        # Verificacao de status detalhado
        elif value["msg"] == "vpn status detalhado prd" or value["msg"] == "vpn status prd detalhado":
            processado = vpn("status detalhado", "sqa")
        # garantindo que o mesmo comando rode caso o usuario digite prod em vez de prd
        elif value["msg"] == "vpn status detalhado prod" or value["msg"] == "vpn status prod detalhado":
            processado = vpn("status detalhado", "sqa")
        
        # Solicitacao de stop
        elif value["msg"] == "vpn stop prd" or value["msg"] == "vpn stop prod":
            processado = vpn("stop", "prd")

        # Solicitacao de start
        elif value["msg"] == "vpn start prd" or value["msg"] == "vpn start prod":
            processado = vpn("start", "prd")

        # Solicitacao de restart
        elif value["msg"] == "vpn restart prd" or value["msg"] == "vpn restart prod":
            processado = vpn("restart", "prd")

        # Hora certa ;)
        elif value["msg"] == "hora certa":
            processado = "Agora sao " + strftime("%H:%M:%S", localtime())
        
        # Se tudo der errado, listar as possibilidades de comandos
        else:
            processado = "Utilize um dos comandos:\nvpn status sqa\nvpn status prd\nvpn status detalhado sqa\nvpn status detalhado prd\nvpn [stop|start|restart] [sqa|prd|prod]\nhora certa\n"

        payload = {'channel': value['channel'], 'user': value['user'], 'msg': processado, 'bot_id': value['bot_id']}
        send_queue(rabbit_queue_push, payload)


if __name__ == '__main__':
    print("Programa iniciado")
    
    main()

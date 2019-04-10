#!/usr/bin/python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import puka
import json
import time

from config import *


def connect_slack():
    sc = SlackClient(slack_client)
    sc.rtm_connect()
    return sc

# valida se a mensagem é para mim, o CHANNEL[0] == "D" significa que o bot pode receber uma menssagem no privado sem o @
# Verificar se a msg é para mim
def is_for_me(event, bot_id):
    type = event.get('type')
    try:
        if type == 'message':
            text = event.get('text')
            channel = event.get('channel')
            user = event.get('user')
            if str(bot_id) in str(text):
                return True
            if str(channel[0]) == "D" and str(user) != bot_id_cleand:
                return True
    except:
        return None


def send_queue(queue, payload):
    producer = puka.Client(rabbitmq)
    send_promise = producer.connect()
    producer.wait(send_promise)
    send_promise = producer.queue_declare(queue=queue)
    producer.wait(send_promise)
    # send message to the queue named rabbit
    send_promise = producer.basic_publish(exchange='', routing_key=rabbit_queue, body=json.dumps(payload))
    producer.wait(send_promise)
    return True


def main():
    sc = connect_slack()
    while True:
        for slack_message in sc.rtm_read():
            message = slack_message.get("text")
            user = slack_message.get("user")
            channel = slack_message.get('channel')
# Verificar se a msg é para mim
            for_me = is_for_me(slack_message, bot_id)
            if for_me:
                payload = {'channel': channel, 'user': user, 'msg': message, 'bot_id': bot_id}
                send_queue(rabbit_queue, payload)


if __name__ == '__main__':
    print("Programa iniciado")
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from slackclient import SlackClient
import time
import puka
import json


from config import *



def connect_slack():
    sc = SlackClient(slack_client)
    sc.rtm_connect()
    return sc

def send_menssage(sc, channel, msg):  
    sc.rtm_send_message(channel, msg)

def main():
    sc = connect_slack()
    consumer = puka.Client(rabbitmq)
    receive_promise = consumer.connect()
    consumer.wait(receive_promise)
    receive_promise = consumer.basic_consume(queue=rabbit_queue, no_ack=True)

    while True:
        received_message = consumer.wait(receive_promise)
        value = json.loads(received_message['body'])
        send_menssage(sc, str(value["channel"]), str(value["msg"]))            


if __name__ == '__main__':
    print("Programa iniciado")
    main()

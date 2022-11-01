import sys
from python_banyan.banyan_base import BanyanBase


class SecondaryFirstServer(BanyanBase):

    def __init__(self, top):
        super(SecondaryFirstServer, self).__init__(process_name='Sec1Server')
        self.topic = top
        self.set_subscriber_topic(self.topic)
        self.MESSAGES = []

        print("\nSECONDARY 1 started\n")
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)


    def incoming_message_processing(self, topic, payload):
        if payload['command'] == 'APPEND':
            self.MESSAGES.append(f"{payload['message_number']} {payload['message_text']}")

        print(f"{self.topic} received and APPEND message: {payload}")


def server():
    SecondaryFirstServer('secondary1')


if __name__ == '__main__':
    server()
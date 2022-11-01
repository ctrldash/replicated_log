
import sys
import random
import string
from python_banyan.banyan_base import BanyanBase


class EchoClient(BanyanBase):
    '''Will send some msgs'''

    def __init__(self):

        super(EchoClient, self).__init__(process_name='EchoClient')

        self.set_subscriber_topic('reply')

        self.message_number = self.number_of_messages = 10

        # send first message
        self.publish_payload(
            {'message_number': self.message_number, 
             'command': 'APPEND',
             'message_text': 'init'},
            'command')

        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)


    def incoming_message_processing(self, topic, payload):

        if self.message_number == 0:
            print(str(self.number_of_messages) + ' messages sent and received. Finish bombarding.')
            input('Press enter to exit.')
            self.clean_up()
            sys.exit(0)
        
        elif self.message_number % 3 == 0:
            print(f"Sending command LIST MESSAGES on {self.message_number}")
            
            if self.message_number >= 0:
                txt = ''.join(random.sample(string.ascii_lowercase, 8))
                sending_payload = {
                    'message_text': txt,
                    'message_number': self.message_number,
                    'command': 'LIST',
                    }
                self.publish_payload(sending_payload, 'command')
                self.message_number -= 1

        else:
            if self.message_number >= 0:
                txt = ''.join(random.sample(string.ascii_lowercase, 8))
                sending_payload = {
                    'message_text': txt,
                    'message_number': self.message_number,
                    'command': 'APPEND',
                    }
                self.publish_payload(sending_payload, 'command')
                self.message_number -= 1


def echo_client():
    EchoClient()


if __name__ == '__main__':
    echo_client()
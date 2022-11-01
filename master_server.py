import sys
from python_banyan.banyan_base import BanyanBase


class MasterServer(BanyanBase):

    def __init__(self, ):
        super(MasterServer, self).__init__(process_name='EchoServer')
        print('\nMASTER  started\n')
        self.SECONDARY1 = 'secondary1'  # 43126
        self.SECONDARY2 = 'secondary2'  # 43127

        self.set_subscriber_topic('command')  # echo
        self.MESSAGES = []

        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)


    def incoming_message_processing(self, topic, payload):
        print('Received message number:', payload['message_number'])

        if payload['command'] == 'APPEND':
            
            self.MESSAGES.append(f"{payload['message_number']} {payload['message_text']}")
            self.send_to_secondary(payload, self.SECONDARY1)
            self.send_to_secondary(payload, self.SECONDARY2)
    
        elif payload['command'] == 'LIST':
            print(f"\n{'*'* 14} LISTING saved messages{'*'* 14}")
            print(' \n'.join(self.MESSAGES) + '\n' + '*'*40)

        reply_payload = payload
        reply_payload['Executed'] = f"Command {payload['command']} on message: {payload['message_number']}"
        self.publish_payload(reply_payload, 'reply')
        
    
    def send_to_secondary(self, payload, secondary):
        self.publish_payload(payload, secondary)


def echo_server():
    MasterServer()


if __name__ == '__main__':
    echo_server()
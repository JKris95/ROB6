import socket

class Player():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, name = 'player', speed = 1, control_mode = 'fourway'):
        self.name = name
        self.speed = speed
        self.control_mode = control_mode

    def choose_bot38(self):
        self.robot_choice = '192.168.1.38'
    def choose_bot39(self):
        self.robot_choice = '192.168.1.38'

    def Connect(self, HOST, PORT, socket_object):
        """Connects to the desired turtlebot corresponding to the ip-address
        passed to it"""
        try:
            socket_object.connect((HOST, PORT))
        except:
            print("Couldn't connect to TurtleBot with address " + HOST)
            
    def drive(self):
        pass

if __name__ == '__main__':
    kwargs = {"name": "martin", "speed": 0.5}
    player1 = Player(**kwargs)
    print(player1.name, player1.control_mode)
class Player():
    def __init__(self, name = 'player', lin_scale = 1, ang_scale = 1, control_mode = 'four_way', robot = '192.168.1.38', image = ""):
        self.max_lin_speed = 0.22
        self.max_ang_speed = 2.84
        self.name = name
        #self.speeds = {}
        self.lin_speed = lin_scale * self.max_lin_speed
        self.ang_speed = ang_scale * self.max_ang_speed
        self.control_mode = control_mode
        self.robot = robot
        self.image = image
        self.flip_directions = False

    def set_angular(self, ang_lin=0.8, ang_ang=0.2):
        self.ang_lin = ang_lin * self.lin_speed #New linear speed for curved movement
        self.ang_ang = ang_ang * self.ang_speed #New angular speed for curved movement    
    def easy(self):
        self.lin_speed = 1.0 * self.max_lin_speed
        self.ang_speed = 0.25 * self.max_ang_speed
        self.control_mode = 'eight_way'
        self.set_angular()
    def medium(self):
        self.lin_speed = 0.8 * self.max_lin_speed
        self.ang_speed = 0.5 * self.max_ang_speed
        self.control_mode = 'four_way'
        #self.set_angular() 
    def hard(self):
        self.lin_speed = 0.6 * self.max_lin_speed
        self.ang_speed = 0.75 * self.max_ang_speed
        self.control_mode = 'four_way'
        #self.set_angular()
    def very_hard(self):
        self.lin_speed = 0.4 * self.max_lin_speed
        self.ang_speed = 1.0 * self.max_ang_speed
        self.control_mode = 'angular'
        self.set_angular()
    def new_difficulty(self, difficulty_params):
        """Function intended to create a new difficulty based on
        difficulty parameters from a dictionary"""
        self.lin_speed = difficulty_params['lin_scale'] * self.max_lin_speed
        self.ang_speed = difficulty_params['ang_scale'] * self.max_ang_speed
        self.control_mode = difficulty_params['control_mode']
        self.set_angular()
    
    

if __name__ == '__main__':
    kwargs = {"name": "martin", "lin_scale": 0.5}
    player1 = Player(**kwargs)
    print(player1.lin_speed, player1.ang_speed, player1.control_mode)
    player1.medium()
    print(player1.lin_speed, player1.ang_speed, player1.control_mode)




class GateManeuver(self):
    def __init__(self):
        self.horizontal_move = {0: 'none', -1: 'left', 1: 'right'}
        self.vertical_movement = {-1: 'down', 0: 'staying', 1: 'up'}
        self.rotation_movement = {-1: 'left', 0: 'staying', 1: 'right'}
        self.move_forward = 'forward'
        self.is_forward_done = False
        self.start_pole = False
        self.rotation_angle = 15
        self.pole_rotation = 80
        self.depth_change = 1
        self.depth = -1
        self.sweep = 0
        self.sweep_direction = {0: 'right', 1: 'left'}

    def move_to_gate(self, navigation, coordinates, power, rotation):
        navigation.h_nav(self.vertical_movement[coordinates[1]], self.depth_change, 100)
        navigation.r_nav(self.rotation_movement[coordinates[0]], self.rotation_angle, power)
        navigation.m_nav('power', self.move_forward, power)

    def pole(self, navigation, power):
        navigation.r_nav('right', 45, self.pole_rotation)
        navigation.ros_sleep(1)

        navigation.cancel_r_nav()
        navigation.m_nav('power', self.move_forward, power)
        navigation.ros_sleep(2)

        navigation.cancel_m_nav()
        navigation.r_nav('left', 90, self.pole_rotation)
        navigation.ros_sleep(1)

        navigation.cancel_r_nav()
        navigation.m_nav('power', self.move_forward, power)
        navigation.ros_sleep(2)

        navigation.cancel_m_nav()
        navigation.r_nav('left', 90, self.pole_rotation)
        navigation.ros_sleep(1)

        navigation.cancel_r_nav()
        navigation.m_nav('power', self.move_forward, power)
        navigation.ros_sleep(2)

        navigation.cancel_m_nav()
        navigation.r_nav('left', 90, self.pole_rotation)
        navigation.ros_sleep(1)

        navigation.cancel_r_nav()
        navigation.m_nav('power', self.move_forward, power)
        navigation.ros_sleep(2)

        navigation.cancel_m_nav()
        navigation.r_nav('right', 45, self.pole_rotation)
        navigation.ros_sleep(1)

        navigation.cancel_r_nav()
        move_forward()
    
    def move_forward(self, navigation, power):
        navigation.m_nav('power', self.move_forward, power)
        navigation.ros_sleep(5)
        self.is_forward_done = True
        self.start_pole = !self.start_pole

    def sweep(self, navigation, power, rotation):
        navigation.r_nav(self.sweep_direction[self.sweep], rotation, 50)
        navigation.m_nav('power', self.move_forward, power)
        ''' used to change 0 to 1 and 1 to 0 without using if statements'''
        self.sweep = 1 - self.sweep
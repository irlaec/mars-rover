import unittest
from main import MarsMission, Rover, Plateau


class TestMarsMission(unittest.TestCase):
    def test_main_case(self):
        input_example = "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM"
        mission = MarsMission(input_example)
        mission.start()

        self.assertEqual(mission.get_output(), "1 3 N\n5 1 E\n")

    def test_rover_turns(self):
        pos_x = '0'
        pox_y = '0'
        rover = Rover(plateau=None, pos_x=pos_x, pos_y=pos_x, cardinal_point='N')
        rover.move(instructions='L')
        self.assertEqual(rover.get_position(), f"{pos_x} {pox_y} W")

        rover.move(instructions='RRR')
        self.assertEqual(rover.get_position(), f"{pos_x} {pox_y} S")

    def test_rover_moves(self):
        pos_x = '0'
        pox_y = '0'
        plateau = Plateau(upper=5, right=5)
        rover = Rover(plateau=plateau, pos_x=pos_x, pos_y=pos_x, cardinal_point='N')
        rover.move(instructions='M')
        self.assertEqual(rover.get_position(), f"{pos_x} {int(pox_y) + 1} N")

    def test_rover_limit_hit(self):
        pos_x = '0'
        pox_y = '0'
        plateau = Plateau(upper=5, right=5)
        rover = Rover(plateau=plateau, pos_x=pos_x, pos_y=pos_x, cardinal_point='S')
        rover.move(instructions='M')
        self.assertEqual(rover.get_position(), f"{pos_x} {pox_y} S")

        rover.move(instructions='RM')
        self.assertEqual(rover.get_position(), f"{pos_x} {pox_y} W")

    def test_plateau_valid_position(self):
        plateau = Plateau(upper=5, right=5)
        self.assertEqual(plateau.is_valid_position(pos_x=0, pos_y=-1), False)
        self.assertEqual(plateau.is_valid_position(pos_x=0, pos_y=0), True)
        self.assertEqual(plateau.is_valid_position(pos_x=5, pos_y=5), True)
        self.assertEqual(plateau.is_valid_position(pos_x=5, pos_y=6), False)


if __name__ == "__main__":
    unittest.main()

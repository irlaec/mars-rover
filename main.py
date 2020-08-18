import numpy as np

CARDINAL_POINTS_ORDERED = ['N', 'E', 'S', 'W']


class Rover:
    def __init__(self, plateau, pos_x: str, pos_y: str, cardinal_point: str):
        self.plateau = plateau
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.cardinal_point = cardinal_point

    def move(self, instructions: str) -> bool:
        """Moves the rover according to the given instructions"""
        hit_limit = False
        for instruction in instructions:
            hit_limit = False
            if instruction == 'L':
                self._move_l()
            elif instruction == 'R':
                self._move_r()
            elif instruction == 'M':
                hit_limit = self._move_m()
            else:
                print(f'Wrong command for the rover, it will be ignored: {instruction}')

            if hit_limit:
                break

        return hit_limit

    def get_position(self) -> str:
        """Returns the position of the rover formatted"""
        return f'{self.pos_x} {self.pos_y} {self.cardinal_point}'

    def _move_l(self):
        """Makes the rover spin 90° to the left"""
        current_idx = CARDINAL_POINTS_ORDERED.index(self.cardinal_point)
        self.cardinal_point = CARDINAL_POINTS_ORDERED[current_idx - 1]

    def _move_r(self):
        """Makes the rover spin 90° to the right"""
        current_idx = CARDINAL_POINTS_ORDERED.index(self.cardinal_point)
        next_idx = current_idx + 1 if current_idx != 3 else 0
        self.cardinal_point = CARDINAL_POINTS_ORDERED[next_idx]

    def _move_m(self) -> bool:
        """Moves the rover forward one grid point, if possible"""
        next_x = self.pos_x
        next_y = self.pos_y
        hit_limit = False

        if self.cardinal_point == 'N':
            next_y += 1
        elif self.cardinal_point == 'S':
            next_y -= 1
        elif self.cardinal_point == 'E':
            next_x += 1
        elif self.cardinal_point == 'W':
            next_x -= 1

        if self.plateau.is_valid_position(next_x, next_y):
            self.pos_x = next_x
            self.pos_y = next_y
        else:
            hit_limit = True

        return hit_limit


class Plateau:
    def __init__(self, upper: int, right: int):
        self.max_y = int(upper)
        self.max_x = int(right)
        self.grid = np.zeros((self.max_x + 1, self.max_y + 1))

    def save_rover_pos(self, pos_x: int, pos_y: int):
        """Save the position of the rover in the grid"""
        self.grid[pos_x, pos_y] = 1

    def is_valid_position(self, pos_x: int, pos_y: int) -> bool:
        """Checks if a position is valid: is inside of the grid and there's no obstacles in that position."""
        if 0 <= pos_x <= self.max_x and 0 <= pos_y <= self.max_y:
            valid = self.grid[pos_x, pos_y] == 0
        else:
            valid = False
        return valid


class MarsMission:
    def __init__(self, command_input: str):
        self.command_input = command_input
        self.plateau = None
        self.output = ""

    def start(self):
        """Starts the Mars Mission"""
        commands = self._get_command_list()
        self._initialize_plateau(commands.pop(0))
        self._manage_rovers(commands)

    def get_output(self) -> str:
        """Returns the output string of the mission """
        return self.output

    def _get_command_list(self) -> list:
        """Extracts a list of commands from the input command string"""
        return self.command_input.splitlines()

    def _initialize_plateau(self, plateau_coordinates: str):
        """Initializes de plateau with the given size"""
        coordinates = plateau_coordinates.split(' ')
        if len(coordinates) == 2 and all(num.isdigit() for num in coordinates):
            self.plateau = Plateau(*coordinates)
        else:
            raise ValueError('Wrong input for plateau initialization')

    def _manage_rovers(self, rover_commands: list):
        """Creates and manages the rovers according to the given commands"""
        while rover_commands:
            rover_coordinates = rover_commands.pop(0)
            rover = Rover(self.plateau, *rover_coordinates.split(' '))

            rover_instructions = rover_commands.pop(0)
            limit_hit = rover.move(rover_instructions)

            self.plateau.save_rover_pos(rover.pos_x, rover.pos_y)

            if limit_hit:
                print(f'Limit or obstacle hit, stopping rover')

            self.output += rover.get_position() + "\n"


if __name__ == "__main__":
    input_example = "5 5\n1 2 N\nLMLMLMLMM\n3 3 E\nMMRMMRMRRM"
    mission = MarsMission(input_example)
    mission.start()
    print(mission.get_output())

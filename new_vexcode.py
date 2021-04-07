from vexcode import *
from enum import Enum


class Walls(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


class Node:
    unicode_chars = dict([
        (1, ' '),  # Walls: None
        (2, '│'),  # Walls: North
        (3, '─'),  # Walls: East
        (5, '│'),  # Walls: South
        (6, '└'),  # Walls: North, East
        (7, '─'),  # Walls: West
        (10, '│'),  # Walls: North, South
        (14, '┘'),  # Walls: North, West
        (15, '┌'),  # Walls: East, South
        (21, '─'),  # Walls: East, West
        (30, '├'),  # Walls: North, East, South
        (35, '┐'),  # Walls: South, West
        (42, '┴'),  # Walls: North, East, West
        (70, '┤'),  # Walls: North, South, West
        (105, '┬'),  # Walls: East, South, West
        (210, '┼'),  # Walls: North, East, South, West
    ])

    def __init__(self):
        self.north_node = None
        self.east_node = None
        self.south_node = None
        self.west_node = None

    def get_unicode_char(self):
        node_state = 1
        if self.north_node is not None: node_state *= 2
        if self.east_node is not None: node_state *= 3
        if self.south_node is not None: node_state *= 5
        if self.west_node is not None: node_state *= 7
        return self.unicode_chars[node_state]


class Cell:
    def __init__(self, x_pos, y_pos, maze):
        self.x_position = x_pos
        self.y_position = y_pos
        self.maze = maze

        self.top_right_node = None
        self.top_left_node = None
        self.bottom_left_node = None
        self.bottom_right_node = None

        self.north_cell = None
        self.east_cell = None
        self.south_cell = None
        self.west_cell = None

    def initialize_cells(self):
        self.top_right_node = self.maze.nodes[self.x_position + 1][self.y_position + 1]
        self.top_left_node = self.maze.nodes[self.x_position][self.y_position + 1]
        self.bottom_left_node = self.maze.nodes[self.x_position][self.y_position]
        self.bottom_right_node = self.maze.nodes[self.x_position + 1][self.y_position]

        self.north_cell = self.maze.cells[self.x_position][self.y_position + 1] if self.y_position + 1 < self.maze.height else None
        self.east_cell = self.maze.cells[self.x_position + 1][self.y_position] if self.x_position + 1 < self.maze.width else None
        self.south_cell = self.maze.cells[self.x_position][self.y_position - 1] if self.y_position - 1 >= 0 else None
        self.west_cell = self.maze.cells[self.x_position - 1][self.y_position] if self.x_position - 1 >= 0 else None

    def update_north(self, state):
        if state:
            self.top_right_node.west_node = self.top_left_node
            self.top_left_node.east_node = self.top_right_node

    def update_east(self, state):
        if state:
            self.top_right_node.south_node = self.bottom_right_node
            self.bottom_right_node.north_node = self.top_right_node

    def update_south(self, state):
        if state:
            self.bottom_right_node.west_node = self.bottom_left_node
            self.bottom_left_node.east_node = self.bottom_right_node

    def update_west(self, state):
        if state:
            self.top_left_node.south_node = self.bottom_left_node
            self.bottom_left_node.north_node = self.top_left_node

    def check_wall(self, wall):
        if wall == Walls.North: return self.top_right_node.west_node is not None and self.top_left_node.east_node is not None
        if wall == Walls.East: return self.top_right_node.south_node is not None and self.bottom_right_node.north_node is not None
        if wall == Walls.South: return self.bottom_right_node.west_node is not None and self.bottom_left_node.east_node is not None
        if wall == Walls.West: return self.top_left_node.south_node is not None and self.bottom_left_node.north_node is not None
        # throw new InvalidEnumArgumentException() :(

    def get_unicode_char(self, wall):
        if wall == Walls.North:
            if self.check_wall(wall):
                return '─'
            else:
                return ' '
        if wall == Walls.East:
            if self.check_wall(wall):
                return '│'
            else:
                return ' '
        if wall == Walls.South:
            if self.check_wall(wall):
                return '─'
            else:
                return ' '
        if wall == Walls.West:
            if self.check_wall(wall):
                return '│'
            else:
                return ' '
        # throw new InvalidEnumArgumentException() :(


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.cells = []
        self.nodes = []

    def initialize_maze(self):
        for x_pos in range(self.width):
            self.cells.append([])
            for y_pos in range(self.height):
                self.cells[x_pos].append(Cell(x_pos, y_pos, self))

        for x_pos in range(self.width + 1):
            self.nodes.append([])
            for y_pos in range(self.height + 1):
                self.nodes[x_pos].append(Node())

        for cell_array in self.cells:
            for cell in cell_array:
                cell.initialize_cells()

    def update_cell(self, x_pos, y_pos, wall, state):
        if wall == Walls.North:
            self.cells[x_pos][y_pos].update_north(state)
            incremented_y = y_pos + 1
            if incremented_y < self.height: self.cells[x_pos][incremented_y].update_south(state)
        if wall == Walls.East:
            self.cells[x_pos][y_pos].update_east(state)
            incremented_x = x_pos + 1
            if incremented_x < self.width: self.cells[incremented_x][y_pos].update_west(state)
        if wall == Walls.South:
            self.cells[x_pos][y_pos].update_south(state)
            decremented_y = y_pos - 1
            if decremented_y >= 0: self.cells[x_pos][decremented_y].update_north(state)
        if wall == Walls.West:
            self.cells[x_pos][y_pos].update_west(state)
            decremented_x = x_pos - 1
            if decremented_x >= 0: self.cells[decremented_x][y_pos].update_east(state)

    def pathfind_breath_first(self, x_start, y_start, x_end, y_end):
        stack = []
        visited_cells = {}

        start_cell = self.cells[x_start][y_start]
        end_cell = self.cells[x_end][y_end]

        stack.append(start_cell)
        visited_cells[start_cell] = start_cell

        while end_cell not in visited_cells:
            current_cell = stack.pop(0)

            if current_cell.north_cell is not None and current_cell.north_cell not in visited_cells and not current_cell.check_wall(Walls.North):
                stack.append(current_cell.north_cell)
                visited_cells[current_cell.north_cell] = current_cell

            if current_cell.east_cell is not None and current_cell.east_cell not in visited_cells and not current_cell.check_wall(Walls.East):
                stack.append(current_cell.east_cell)
                visited_cells[current_cell.east_cell] = current_cell

            if current_cell.south_cell is not None and current_cell.south_cell not in visited_cells and not current_cell.check_wall(Walls.South):
                stack.append(current_cell.south_cell)
                visited_cells[current_cell.south_cell] = current_cell

            if current_cell.west_cell is not None and current_cell.west_cell not in visited_cells and not current_cell.check_wall(Walls.West):
                stack.append(current_cell.west_cell)
                visited_cells[current_cell.west_cell] = current_cell

        tracing_cell = end_cell
        path_points = []
        while visited_cells[tracing_cell] is not tracing_cell:
            tracing_cell = visited_cells[tracing_cell]
            path_points.append((tracing_cell.x_position, tracing_cell.y_position))
        path_points.reverse()
        path_points.append((x_end, y_end))

        return path_points

    def print_plain(self):
        for x_pos in range(self.width):
            brain_print(self.nodes[x_pos][self.height].get_unicode_char())
            decremented_height = self.height - 1
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
        brain_print(self.nodes[self.width][self.height].get_unicode_char())

        for y_pos in reversed(range(self.height)):
            brain_newline()
            for x_pos in range(self.width):
                brain_print(self.cells[x_pos][y_pos].get_unicode_char(Walls.West))
                brain_print(' ')
                brain_print(' ')
                brain_print(' ')
            decremented_width = self.width - 1
            brain_print(self.cells[decremented_width][y_pos].get_unicode_char(Walls.East))

            brain_newline()
            for x_pos in range(self.width):
                brain_print(self.nodes[x_pos][y_pos].get_unicode_char())
                brain_print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
                brain_print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
                brain_print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
            brain_print(self.nodes[self.width][y_pos].get_unicode_char())

    def print_path(self, path, path_char):
        for x_pos in range(self.width):
            brain_print(self.nodes[x_pos][self.height].get_unicode_char())
            decremented_height = self.height - 1
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain_print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
        brain_print(self.nodes[self.width][self.height].get_unicode_char())

        for y_pos in reversed(range(self.height)):
            brain_newline()
            for x_pos in range(self.width):
                wall_char = self.cells[x_pos][y_pos].get_unicode_char(Walls.West)
                mid_in_path = (x_pos, y_pos) in path
                wall_in_path = wall_char == ' ' and mid_in_path and (x_pos - 1, y_pos) in path
                brain_print(path_char if wall_in_path else wall_char)
                brain_print(' ')
                brain_print(path_char if mid_in_path else ' ')
                brain_print(' ')
            decremented_width = self.width - 1
            brain_print(self.cells[decremented_width][y_pos].get_unicode_char(Walls.East))

            brain_newline()
            for x_pos in range(self.width):
                wall_char = self.cells[x_pos][y_pos].get_unicode_char(Walls.South)
                wall_in_path = wall_char == ' ' and (x_pos, y_pos) in path and (x_pos, y_pos - 1) in path  # Might have check for x_pos == 0
                brain_print(self.nodes[x_pos][y_pos].get_unicode_char())
                brain_print(wall_char)
                brain_print(path_char if wall_in_path else wall_char)
                brain_print(wall_char)
            brain_print(self.nodes[self.width][y_pos].get_unicode_char())


def set_map(maze_instance):
    maze_instance.update_cell(0, 0, Walls.South, True)
    maze_instance.update_cell(1, 0, Walls.South, True)
    maze_instance.update_cell(2, 0, Walls.South, True)
    maze_instance.update_cell(3, 0, Walls.South, True)
    maze_instance.update_cell(4, 0, Walls.South, False)
    maze_instance.update_cell(5, 0, Walls.South, True)
    maze_instance.update_cell(6, 0, Walls.South, True)
    maze_instance.update_cell(7, 0, Walls.South, True)

    maze_instance.update_cell(0, 0, Walls.West, True)
    maze_instance.update_cell(1, 0, Walls.West, True)
    maze_instance.update_cell(2, 0, Walls.West, False)
    maze_instance.update_cell(3, 0, Walls.West, True)
    maze_instance.update_cell(4, 0, Walls.West, False)
    maze_instance.update_cell(5, 0, Walls.West, True)
    maze_instance.update_cell(6, 0, Walls.West, False)
    maze_instance.update_cell(7, 0, Walls.West, False)

    maze_instance.update_cell(7, 0, Walls.East, True)

    maze_instance.update_cell(0, 1, Walls.South, False)
    maze_instance.update_cell(1, 1, Walls.South, False)
    maze_instance.update_cell(2, 1, Walls.South, False)
    maze_instance.update_cell(3, 1, Walls.South, False)
    maze_instance.update_cell(4, 1, Walls.South, False)
    maze_instance.update_cell(5, 1, Walls.South, False)
    maze_instance.update_cell(6, 1, Walls.South, True)
    maze_instance.update_cell(7, 1, Walls.South, False)

    maze_instance.update_cell(0, 1, Walls.West, True)
    maze_instance.update_cell(1, 1, Walls.West, True)
    maze_instance.update_cell(2, 1, Walls.West, True)
    maze_instance.update_cell(3, 1, Walls.West, False)
    maze_instance.update_cell(4, 1, Walls.West, True)
    maze_instance.update_cell(5, 1, Walls.West, False)
    maze_instance.update_cell(6, 1, Walls.West, True)
    maze_instance.update_cell(7, 1, Walls.West, False)

    maze_instance.update_cell(7, 1, Walls.East, True)

    maze_instance.update_cell(0, 2, Walls.South, False)
    maze_instance.update_cell(1, 2, Walls.South, False)
    maze_instance.update_cell(2, 2, Walls.South, True)
    maze_instance.update_cell(3, 2, Walls.South, False)
    maze_instance.update_cell(4, 2, Walls.South, True)
    maze_instance.update_cell(5, 2, Walls.South, False)
    maze_instance.update_cell(6, 2, Walls.South, False)
    maze_instance.update_cell(7, 2, Walls.South, True)

    maze_instance.update_cell(0, 2, Walls.West, True)
    maze_instance.update_cell(1, 2, Walls.West, False)
    maze_instance.update_cell(2, 2, Walls.West, True)
    maze_instance.update_cell(3, 2, Walls.West, False)
    maze_instance.update_cell(4, 2, Walls.West, False)
    maze_instance.update_cell(5, 2, Walls.West, True)
    maze_instance.update_cell(6, 2, Walls.West, True)
    maze_instance.update_cell(7, 2, Walls.West, False)

    maze_instance.update_cell(7, 2, Walls.East, True)

    maze_instance.update_cell(0, 3, Walls.South, False)
    maze_instance.update_cell(1, 3, Walls.South, False)
    maze_instance.update_cell(2, 3, Walls.South, False)
    maze_instance.update_cell(3, 3, Walls.South, True)
    maze_instance.update_cell(4, 3, Walls.South, True)
    maze_instance.update_cell(5, 3, Walls.South, False)
    maze_instance.update_cell(6, 3, Walls.South, True)
    maze_instance.update_cell(7, 3, Walls.South, False)

    maze_instance.update_cell(0, 3, Walls.West, True)
    maze_instance.update_cell(1, 3, Walls.West, False)
    maze_instance.update_cell(2, 3, Walls.West, False)
    maze_instance.update_cell(3, 3, Walls.West, True)
    maze_instance.update_cell(4, 3, Walls.West, False)
    maze_instance.update_cell(5, 3, Walls.West, True)
    maze_instance.update_cell(6, 3, Walls.West, False)
    maze_instance.update_cell(7, 3, Walls.West, True)

    maze_instance.update_cell(7, 3, Walls.East, True)

    maze_instance.update_cell(0, 4, Walls.South, False)
    maze_instance.update_cell(1, 4, Walls.South, True)
    maze_instance.update_cell(2, 4, Walls.South, False)
    maze_instance.update_cell(3, 4, Walls.South, False)
    maze_instance.update_cell(4, 4, Walls.South, False)
    maze_instance.update_cell(5, 4, Walls.South, True)
    maze_instance.update_cell(6, 4, Walls.South, False)
    maze_instance.update_cell(7, 4, Walls.South, False)

    maze_instance.update_cell(0, 4, Walls.West, True)
    maze_instance.update_cell(1, 4, Walls.West, True)
    maze_instance.update_cell(2, 4, Walls.West, False)
    maze_instance.update_cell(3, 4, Walls.West, True)
    maze_instance.update_cell(4, 4, Walls.West, True)
    maze_instance.update_cell(5, 4, Walls.West, False)
    maze_instance.update_cell(6, 4, Walls.West, True)
    maze_instance.update_cell(7, 4, Walls.West, True)

    maze_instance.update_cell(7, 4, Walls.East, True)

    maze_instance.update_cell(0, 5, Walls.South, True)
    maze_instance.update_cell(1, 5, Walls.South, False)
    maze_instance.update_cell(2, 5, Walls.South, False)
    maze_instance.update_cell(3, 5, Walls.South, False)
    maze_instance.update_cell(4, 5, Walls.South, True)
    maze_instance.update_cell(5, 5, Walls.South, False)
    maze_instance.update_cell(6, 5, Walls.South, False)
    maze_instance.update_cell(7, 5, Walls.South, False)

    maze_instance.update_cell(0, 5, Walls.West, True)
    maze_instance.update_cell(1, 5, Walls.West, False)
    maze_instance.update_cell(2, 5, Walls.West, True)
    maze_instance.update_cell(3, 5, Walls.West, False)
    maze_instance.update_cell(4, 5, Walls.West, True)
    maze_instance.update_cell(5, 5, Walls.West, False)
    maze_instance.update_cell(6, 5, Walls.West, False)
    maze_instance.update_cell(7, 5, Walls.West, True)

    maze_instance.update_cell(7, 5, Walls.East, True)

    maze_instance.update_cell(0, 6, Walls.South, False)
    maze_instance.update_cell(1, 6, Walls.South, False)
    maze_instance.update_cell(2, 6, Walls.South, True)
    maze_instance.update_cell(3, 6, Walls.South, True)
    maze_instance.update_cell(4, 6, Walls.South, False)
    maze_instance.update_cell(5, 6, Walls.South, True)
    maze_instance.update_cell(6, 6, Walls.South, True)
    maze_instance.update_cell(7, 6, Walls.South, False)

    maze_instance.update_cell(0, 6, Walls.West, True)
    maze_instance.update_cell(1, 6, Walls.West, True)
    maze_instance.update_cell(2, 6, Walls.West, False)
    maze_instance.update_cell(3, 6, Walls.West, False)
    maze_instance.update_cell(4, 6, Walls.West, True)
    maze_instance.update_cell(5, 6, Walls.West, True)
    maze_instance.update_cell(6, 6, Walls.West, False)
    maze_instance.update_cell(7, 6, Walls.West, True)

    maze_instance.update_cell(7, 6, Walls.East, True)

    maze_instance.update_cell(0, 7, Walls.South, False)
    maze_instance.update_cell(1, 7, Walls.South, True)
    maze_instance.update_cell(2, 7, Walls.South, True)
    maze_instance.update_cell(3, 7, Walls.South, False)
    maze_instance.update_cell(4, 7, Walls.South, False)
    maze_instance.update_cell(5, 7, Walls.South, False)
    maze_instance.update_cell(6, 7, Walls.South, False)
    maze_instance.update_cell(7, 7, Walls.South, False)

    maze_instance.update_cell(0, 7, Walls.West, True)
    maze_instance.update_cell(1, 7, Walls.West, False)
    maze_instance.update_cell(2, 7, Walls.West, False)
    maze_instance.update_cell(3, 7, Walls.West, True)
    maze_instance.update_cell(4, 7, Walls.West, True)
    maze_instance.update_cell(5, 7, Walls.West, False)
    maze_instance.update_cell(6, 7, Walls.West, True)
    maze_instance.update_cell(7, 7, Walls.West, False)

    maze_instance.update_cell(7, 7, Walls.East, True)

    maze_instance.update_cell(0, 7, Walls.North, True)
    maze_instance.update_cell(1, 7, Walls.North, True)
    maze_instance.update_cell(2, 7, Walls.North, True)
    maze_instance.update_cell(3, 7, Walls.North, False)
    maze_instance.update_cell(4, 7, Walls.North, True)
    maze_instance.update_cell(5, 7, Walls.North, True)
    maze_instance.update_cell(6, 7, Walls.North, True)
    maze_instance.update_cell(7, 7, Walls.North, True)


def brain_print(item):
    brain.print(item)
    return


def brain_newline():
    brain.new_line()
    return


def get_current_cell_location():
    x_pos = location.position(X, MM) + 1000
    y_pos = location.position(Y, MM) + 1000

    x_cell = x_pos // 250
    y_cell = y_pos // 250
    return (x_cell, y_cell)


def get_facing_wall():
    heading = drivetrain.heading(DEGREES)
    if heading > 315 or heading < 45:
        return Walls.North

    if heading >= 45 and heading < 135:
        return Walls.East
    if heading >= 135 and heading < 225:
        return Walls.South
    if heading >= 225 and heading < 315:
        return Walls.West


def update_facing_wall():
    global maze
    current_location = get_current_cell_location()
    facing_wall = get_facing_wall()
    wall_state = distance.get_distance(MM) < 150
    maze.update_cell(current_location[0], current_location[1], facing_wall, wall_state)


def check_left():
    drivetrain.turn_for(LEFT, 90, DEGREES)


maze = Maze(8, 8)


# Add project code in "main"
def main():
    global maze
    maze.initialize_maze()

    drivetrain.set_drive_velocity(100, PERCENT)  # speeds up the robot
    drivetrain.set_turn_velocity(100, PERCENT)

    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()
    check_left()
    brain.print(get_facing_wall())
    brain.new_line()

    maze.print_plain()


# VR threads — Do not delete
vr_thread(main())
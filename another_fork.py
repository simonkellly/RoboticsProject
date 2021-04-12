from enum import IntEnum
from vexcode import *


class Walls(IntEnum):
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

        self.north_known = False
        self.east_known = False
        self.south_known = False
        self.west_known = False

        self.north_visited = 0
        self.east_visited = 0
        self.south_visited = 0
        self.west_visited = 0

        self.north_forced = False
        self.east_forced = False
        self.south_forced = False
        self.west_forced = False

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

    def visit_wall(self, wall):
        if wall == Walls.North:
            self.top_right_node.west_visited += 1
            self.top_left_node.east_visited += 1
        if wall == Walls.East:
            self.top_right_node.south_visited += 1
            self.bottom_right_node.north_visited += 1
        if wall == Walls.South:
            self.bottom_right_node.west_visited += 1
            self.bottom_left_node.east_visited += 1
        if wall == Walls.West:
            self.top_left_node.south_visited += 1
            self.bottom_left_node.north_visited += 1

    def check_visited(self, wall):
        if wall == Walls.North:
            return self.top_right_node.west_visited
        if wall == Walls.East:
            return self.top_right_node.south_visited
        if wall == Walls.South:
            return self.bottom_right_node.west_visited
        if wall == Walls.West:
            return self.top_left_node.south_visited

    def force_wall(self, wall, amount=2):
        for visit in range(amount):
            self.visit_wall(wall)

        if wall == Walls.North:
            self.update_north(False)
            self.top_right_node.west_forced = True
            self.top_left_node.east_forced = True
        if wall == Walls.East:
            self.update_east(False)
            self.top_right_node.south_forced = True
            self.bottom_right_node.north_forced = True
        if wall == Walls.South:
            self.update_south(False)
            self.bottom_right_node.west_forced = True
            self.bottom_left_node.east_forced = True
        if wall == Walls.West:
            self.update_west(False)
            self.top_left_node.south_forced = True
            self.bottom_left_node.north_forced = True

    def check_forced(self, wall):
        if wall == Walls.North:
            return self.top_right_node.west_forced
        if wall == Walls.East:
            return self.top_right_node.south_forced
        if wall == Walls.South:
            return self.bottom_right_node.west_forced
        if wall == Walls.West:
            return self.top_left_node.south_forced

    def update_north(self, state):
        self.top_right_node.west_known = True
        self.top_left_node.east_known = True
        if state:
            self.top_right_node.west_node = self.top_left_node
            self.top_left_node.east_node = self.top_right_node

    def update_east(self, state):
        self.top_right_node.south_known = True
        self.bottom_right_node.north_known = True
        if state:
            self.top_right_node.south_node = self.bottom_right_node
            self.bottom_right_node.north_node = self.top_right_node

    def update_south(self, state):
        self.bottom_right_node.west_known = True
        self.bottom_left_node.east_known = True
        if state:
            self.bottom_right_node.west_node = self.bottom_left_node
            self.bottom_left_node.east_node = self.bottom_right_node

    def update_west(self, state):
        self.top_left_node.south_known = True
        self.bottom_left_node.north_known = True
        if state:
            self.top_left_node.south_node = self.bottom_left_node
            self.bottom_left_node.north_node = self.top_left_node

    def wall_known(self, wall):
        if wall == Walls.North:
            return self.top_right_node.west_known and self.top_left_node.east_known
        if wall == Walls.East:
            return self.top_right_node.south_known and self.bottom_right_node.north_known
        if wall == Walls.South:
            return self.bottom_right_node.west_known and self.bottom_left_node.east_known
        if wall == Walls.West:
            return self.top_left_node.south_known and self.bottom_left_node.north_known

    def fully_known(self):
        top_right_known = self.top_right_node.west_known and self.top_right_node.south_known
        top_left_known = self.top_left_node.east_known and self.top_left_node.south_known
        bottom_right_known = self.bottom_right_node.north_known and self.bottom_right_node.west_known
        bottom_left_known = self.bottom_left_node.east_known and self.bottom_left_node.north_known

        return top_right_known and top_left_known and bottom_right_known and bottom_left_known

    def check_wall(self, wall):
        if wall == Walls.North: return self.top_right_node.west_node is not None and self.top_left_node.east_node is not None
        if wall == Walls.East: return self.top_right_node.south_node is not None and self.bottom_right_node.north_node is not None
        if wall == Walls.South: return self.bottom_right_node.west_node is not None and self.bottom_left_node.east_node is not None
        if wall == Walls.West: return self.top_left_node.south_node is not None and self.bottom_left_node.north_node is not None
        # throw new InvalidEnumArgumentException() :(

    def get_unicode_char(self, wall):
        if not self.wall_known(wall): return '?'
        if not self.check_wall(wall): return self.check_visited(wall)

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
        if x_pos - 1 > len(self.cells) or y_pos - 1 > len(self.cells[x_pos]):
            return

        if x_pos < 0 or y_pos < 0:
            return

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

    def extrapolate_edges(self, cell):
        north = (cell.check_wall(Walls.North) and cell.wall_known(Walls.North)) or cell.check_forced(Walls.North)
        east = (cell.check_wall(Walls.East) and cell.wall_known(Walls.East)) or cell.check_forced(Walls.East)
        south = (cell.check_wall(Walls.South) and cell.wall_known(Walls.South)) or cell.check_forced(Walls.South)
        west = (cell.check_wall(Walls.West) and cell.wall_known(Walls.West)) or cell.check_forced(Walls.West)
        amount_changed = 0
        if not north and east and south and west and not cell.fully_known():
            cell.force_wall(Walls.North)
            amount_changed += 1
        elif north and not east and south and west and not cell.fully_known():
            cell.force_wall(Walls.East)
            amount_changed += 1
        elif north and east and not south and west and not cell.fully_known():
            cell.force_wall(Walls.South)
            amount_changed += 1
        elif north and east and south and not west and not cell.fully_known():
            cell.force_wall(Walls.West)
            amount_changed += 1
        return amount_changed

    def fix_actually_known_corners(self):
        amount_changed = 0
        for cell_arr in self.cells:
            for cell in cell_arr:
                amount_changed += self.extrapolate_edges(cell)
        return amount_changed

    def all_cells_known(self):
        for cell_array in self.cells:
            for cell in cell_array:
                cell_fully_known = cell.fully_known()
                if not cell_fully_known:
                    return False
        return True

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


class Robot:
    def __init__(self, maze, maze_cell_length=250, distance_unit=MM, angle_unit=DEGREES, ):
        drivetrain.set_drive_velocity(100, PERCENT)
        drivetrain.set_turn_velocity(100, PERCENT)

        self.maze = maze
        self.maze_cell_length = maze_cell_length
        self.distance_unit = distance_unit
        self.angle_unit = angle_unit

        self.long_tolerance = 150
        self.short_tolerance = 100
        self.short_turn_offset = 30

    def drive_square(self, forward):
        dir = FORWARD if forward else REVERSE
        drivetrain.drive_for(dir, self.maze_cell_length, self.distance_unit)
        return

    def get_current_cell_location(self):
        x_pos = location.position(X, MM) + 1000
        y_pos = location.position(Y, MM) + 1000

        x_cell = x_pos // 250
        y_cell = y_pos // 250
        return x_cell, y_cell

    def get_current_cell(self):
        cell_location = self.get_current_cell_location()
        return self.maze.cells[cell_location[0]][cell_location[1]]

    def get_facing_wall(self):
        heading = drivetrain.heading(DEGREES)
        if heading > 315 or heading < 45:
            return Walls.North
        if 45 <= heading < 135:
            return Walls.East
        if 135 <= heading < 225:
            return Walls.South
        if 225 <= heading < 315:
            return Walls.West

    def turn_to_wall(self, wall):
        facing_wall = self.get_facing_wall()
        target_wall_heading = (90 * wall) % 360
        drivetrain.turn_to_heading(target_wall_heading, self.angle_unit)
        self.check_full_forward()

    def turn_short_to_wall(self, wall, clockwise):  # clockwise is if you are going clockwise
        target_wall_heading = (90 * wall + self.short_turn_offset)
        if clockwise: target_wall_heading -= 2 * self.short_turn_offset
        target_wall_heading %= 360
        drivetrain.turn_to_heading(target_wall_heading, self.angle_unit)

    def drive_through_wall(self, wall):
        facing_wall = self.get_facing_wall()
        if facing_wall == wall:
            self.turn_to_wall(wall)
            self.drive_square(True)
            return
        if wall % 2 != facing_wall % 2:
            self.turn_to_wall(wall)
            self.drive_square(True)
            return
        self.turn_to_wall((wall + 2) % 4)
        self.drive_square(False)

    def update_forward(self, current_position, step, facing_wall, state):

        if facing_wall == Walls.North:
            if current_position[1] + step >= len(self.maze.cells[current_position[0]]): return
            self.maze.update_cell(current_position[0], current_position[1] + step, facing_wall, state)

        if facing_wall == Walls.East:
            if current_position[0] + step >= len(self.maze.cells): return
            self.maze.update_cell(current_position[0] + step, current_position[1], facing_wall, state)

        if facing_wall == Walls.South:
            if current_position[1] - step < 0: return
            self.maze.update_cell(current_position[0], current_position[1] - step, facing_wall, state)

        if facing_wall == Walls.East:
            if current_position[0] - step < 0: return
            self.maze.update_cell(current_position[0] - step, current_position[1], facing_wall, state)

    def check_long_forward(self):
        current_position = self.get_current_cell_location()
        facing_wall = self.get_facing_wall()
        distance_to_wall = distance.get_distance(self.distance_unit)
        sensor_range = distance_to_wall // 250

        step_zero = distance_to_wall < 150
        self.maze.update_cell(current_position[0], current_position[1], facing_wall, step_zero)
        if sensor_range == 0:
            return self.get_current_cell().check_wall(facing_wall)

        for step in range(1, sensor_range):
            self.update_forward(current_position, step, facing_wall, False)
        self.update_forward(current_position, sensor_range, facing_wall, False)
        return self.get_current_cell().check_wall(facing_wall)

    def check_full_forward(self):
        current_position = self.get_current_cell_location()
        facing_wall = self.get_facing_wall()
        distance_to_wall = distance.get_distance(self.distance_unit)

        state = distance_to_wall < 150
        self.maze.update_cell(current_position[0], current_position[1], facing_wall, state)
        fixed_corners = -1
        while fixed_corners != 0:
            fixed_corners = self.maze.fix_actually_known_corners()
        return self.get_current_cell().check_wall(facing_wall)

        if distance_to_wall > 250:
            self.update_forward(current_position, 0, facing_wall, False)
            if distance_to_wall > 500:
                self.update_forward(current_position, 1, facing_wall, False)
                if distance_to_wall > 750:
                    self.update_forward(current_position, 2, facing_wall, False)
                    if distance_to_wall > 1000:
                        self.update_forward(current_position, 4, facing_wall, False)
                        if distance_to_wall > 1250:
                            self.update_forward(current_position, 5, facing_wall, False)
                            if distance_to_wall > 1500:
                                self.update_forward(current_position, 6, facing_wall, False)
                                if distance_to_wall > 1750:
                                    self.update_forward(current_position, 7, facing_wall, False)
                                else: self.update_forward(current_position, 6, facing_wall, True)
                            else: self.update_forward(current_position, 5, facing_wall, True)
                        else: self.update_forward(current_position, 4, facing_wall, True)
                    else: self.update_forward(current_position, 3, facing_wall, True)
                else: self.update_forward(current_position, 2, facing_wall, True)
            else: self.update_forward(current_position, 1, facing_wall, True)
        else: self.update_forward(current_position, 0, facing_wall, True)

        return self.get_current_cell().check_wall(facing_wall)

    def check_short_forward(self):
        current_position = self.get_current_cell_location()
        facing_wall = self.get_facing_wall()
        distance_to_wall = distance.get_distance(self.distance_unit)
        state = distance_to_wall < self.short_tolerance
        self.maze.update_cell(current_position[0], current_position[1], facing_wall, state)
        fixed_corners = -1
        while fixed_corners != 0:
            fixed_corners = self.maze.fix_actually_known_corners()
        return self.get_current_cell().check_wall(facing_wall)

    def check_junction(self):
        current_cell = self.get_current_cell()
        wall_one_direction = int(self.get_facing_wall())
        wall_zero_direction = (wall_one_direction - 1) % 4
        wall_two_direction = (wall_one_direction + 1) % 4
        wall_three_direction = (wall_one_direction + 2) % 4

        wall_one = self.check_full_forward()

        if current_cell.wall_known(wall_zero_direction):
            wall_zero = current_cell.check_wall(wall_zero_direction)
        else:
            wall_zero = None

        if current_cell.wall_known(wall_two_direction):
            wall_two = current_cell.check_wall(wall_two_direction)
        else:
            wall_two = None

        if current_cell.wall_known(wall_three_direction):
            wall_three = current_cell.check_wall(wall_three_direction)
        else:
            wall_three = None

        if wall_zero is None:
            if wall_three is None:
                self.turn_to_wall(wall_zero_direction)
                wall_zero = self.check_full_forward()
                if wall_two is None:
                    self.turn_to_wall(wall_three_direction)
                    wall_three = self.check_full_forward()
                    self.turn_short_to_wall(wall_two_direction, True)
                    wall_two = self.check_short_forward()
                else:
                    self.turn_short_to_wall(wall_three_direction, False)
                    wall_three = self.check_short_forward()
            elif wall_two is None:
                self.turn_short_to_wall(wall_zero_direction, False)
                wall_zero = self.check_short_forward()
                self.turn_short_to_wall(wall_two_direction, True)
                wall_two = self.check_short_forward()
            else:
                self.turn_short_to_wall(wall_zero_direction, False)
                wall_zero = self.check_short_forward()
        elif wall_two is None:
            if wall_three is None:
                self.turn_to_wall(wall_two_direction)
                wall_two = self.check_full_forward()
                self.turn_short_to_wall(wall_three_direction, True)
                wall_three = self.check_short_forward()
            else:
                self.turn_short_to_wall(wall_two_direction, True)
                wall_two = self.check_short_forward()
        elif wall_three is None:
            self.turn_to_wall(wall_two_direction)
            wall_two = self.check_full_forward()
            self.turn_short_to_wall(wall_three_direction, True)
            wall_three = self.check_short_forward()

        directions_sorted = []  # say line too long so did append
        directions_sorted.append((wall_zero_direction, wall_zero))
        directions_sorted.append((wall_one_direction, wall_one))
        directions_sorted.append((wall_two_direction, wall_two))
        directions_sorted.append((wall_three_direction, wall_three))

        directions_sorted.sort()

        result = []
        for dir in directions_sorted: result.append(dir[1])
        return result

    def tremaux_algorithm(self):
        finished = False
        while not finished:
            fixed_corners = -1
            while fixed_corners != 0:
                fixed_corners = self.maze.fix_actually_known_corners()

            finished = self.maze.all_cells_known()
            if finished: return
            brain.clear()
            self.maze.print_plain()

            current_cell = self.get_current_cell()
            facing_wall = self.get_facing_wall()

            possible_paths = []
            junction_states = self.check_junction()
            for index in range(len(junction_states)):
                if not junction_states[index]:
                    times_visited = current_cell.check_visited(index)
                    possible_paths.append((times_visited, index))

            possible_paths.sort()
            next_direction = None
            min_visited = possible_paths[0][0]
            for pair in possible_paths:
                if pair[1] == facing_wall and pair[0] == min_visited:
                    next_direction = pair[1]

            if next_direction is None:
                for pair in possible_paths:
                    if pair[1] == (facing_wall + 2) % 4 and pair[0] == min_visited:
                        next_direction = pair[1]

            if next_direction is None:
                next_direction = possible_paths[0][1]

            current_cell.visit_wall(next_direction)
            self.drive_through_wall(next_direction)






def set_static_map_data(maze):
    maze.update_cell(0, 0, Walls.South, True)
    maze.update_cell(1, 0, Walls.South, True)
    maze.update_cell(2, 0, Walls.South, True)
    maze.update_cell(3, 0, Walls.South, True)
    maze.update_cell(4, 0, Walls.South, True)
    maze.update_cell(5, 0, Walls.South, True)
    maze.update_cell(6, 0, Walls.South, True)
    maze.update_cell(7, 0, Walls.South, True)

    maze.update_cell(0, 7, Walls.North, True)
    maze.update_cell(1, 7, Walls.North, True)
    maze.update_cell(2, 7, Walls.North, True)
    maze.update_cell(3, 7, Walls.North, True)
    maze.update_cell(4, 7, Walls.North, True)
    maze.update_cell(5, 7, Walls.North, True)
    maze.update_cell(6, 7, Walls.North, True)
    maze.update_cell(7, 7, Walls.North, True)

    maze.update_cell(0, 0, Walls.West, True)
    maze.update_cell(0, 1, Walls.West, True)
    maze.update_cell(0, 2, Walls.West, True)
    maze.update_cell(0, 3, Walls.West, True)
    maze.update_cell(0, 4, Walls.West, True)
    maze.update_cell(0, 5, Walls.West, True)
    maze.update_cell(0, 6, Walls.West, True)
    maze.update_cell(0, 7, Walls.West, True)

    maze.update_cell(7, 0, Walls.East, True)
    maze.update_cell(7, 1, Walls.East, True)
    maze.update_cell(7, 2, Walls.East, True)
    maze.update_cell(7, 3, Walls.East, True)
    maze.update_cell(7, 4, Walls.East, True)
    maze.update_cell(7, 5, Walls.East, True)
    maze.update_cell(7, 6, Walls.East, True)
    maze.update_cell(7, 7, Walls.East, True)


def main():
    maze = Maze(8, 8)
    robot = Robot(maze)

    pen.move(DOWN)
    brain_print_line("Creating maze....")
    maze.initialize_maze()

    drivetrain.set_drive_velocity(1000, PERCENT)
    drivetrain.set_turn_velocity(1000, PERCENT)
    set_static_map_data(maze)

    robot.tremaux_algorithm()

    brain.new_line()
    maze.print_plain()
    brain.new_line()
    path = maze.pathfind_breath_first(4, 0, 3, 7)
    maze.print_path(path, '•')
    brain_print_line("Program Complete")
    stop_project()


def brain_print(item):
    brain.print(item)
    return


def brain_newline():
    brain.new_line()
    return


def brain_print_line(obj):
    brain.new_line()
    brain.print(obj)


# VR threads — Do not delete
vr_thread(main())

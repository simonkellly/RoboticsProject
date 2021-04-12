# =================================================
#
# EEEN10020-Robotics Design Project-2020/21 Spring
#
# Maze Traversing Robot v0.3.0
# Group 18 - Dan Redmond and Simon Kelly
#
# Note: Extra static data that is constant across all the maps is used if competition mode is enabled
# The robot works without it, it just provided a speed boost to the overall mapping.
# =================================================
from enum import IntEnum
from vexcode import *

# COMPETITION_MODE should be enabled if used in the dynamic wall maze or wall-maze playground modes
# The robot functions correctly without it but it provided a speed boost if used
COMPETITION_MODE = True


# The wall enum is used to convert to and from integer values into their corresponding walls
# This makes referring to specific walls more readable, and easier to change if say one were to switch to a hexagon maze
class Walls(IntEnum):
    North = 0
    East = 1
    South = 2
    West = 3


# The node object can be thought of similar to a corner in the maze. It stores information about its connected nodes and various properties.
# Analysis of this allow the robot to infer the state of different walls in the maze so the robot doesn't have to travel there
class Node:
    # This dictionary values allow for the each wall being present to return a different character to be printed when the maze is being displayed
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

    # This constructor initialises the various properties that every node has
    def __init__(self):
        # Each node is linked to four other nodes potentially, A link to another node dictates that in the maze, those two nodes should have a wall between them
        self.north_node = None
        self.east_node = None
        self.south_node = None
        self.west_node = None

        # If the state each part of the node is known, these value is used. This allows for the above nodes to be None and for valid information to still be returned
        self.north_known = False
        self.east_known = False
        self.south_known = False
        self.west_known = False

        # The tremaux algorithm used requires various visited properties to be used on each corridor. This property is kept here rather than on the cell so that multiple cells will not
        # Need to be updated when a wall is visited as they will pull the information directly from a node
        self.north_visited = 0
        self.east_visited = 0
        self.south_visited = 0
        self.west_visited = 0

        # if an edge is calculated to be present or not, that requires the forced property to be set so that the maze can correctly infer the states of any cells which have a non known wall, but many forced walls
        # As these two must have at least one non forced, not present wall so that the area can be traversed
        self.north_forced = False
        self.east_forced = False
        self.south_forced = False
        self.west_forced = False

    # This method will return the unicode character that represents the state of the node
    def get_unicode_char(self):
        node_state = 1
        # Every wall being present causes the node state to be multiplied by a prime number
        # Prime numbers being multiplied together cause unique numbers to be created which can then be used to access the dictionary with the correct unicode character
        if self.north_node is not None: node_state *= 2
        if self.east_node is not None: node_state *= 3
        if self.south_node is not None: node_state *= 5
        if self.west_node is not None: node_state *= 7
        # The character corresponding to the state from the dictionary, is then returned to the calling function
        return self.unicode_chars[node_state]


# Cells in the maze are essentially grid squares with the four walls surrounding it. The cell also has knowledge of its neighbouring cells
# A cell wall is made up of two nodes, with a wall being present if the two nodes are connected. The nodes also store if they know what their value is
# so that when checking if all the walls in a cell are known, it allows for nodes to not be connected and for the robot to know their definite state
class Cell:
    # The cells constructor is used to let the cell know of the maze and its position inside of it
    def __init__(self, x_pos, y_pos, maze):
        self.x_position = x_pos
        self.y_position = y_pos
        self.maze = maze

        # The cell is also linked to a set of nodes, one for each of its corners
        self.top_right_node = None
        self.top_left_node = None
        self.bottom_left_node = None
        self.bottom_right_node = None

        # Neighbouring cells will also be linked to each other in order in the initialize function to allow updates between multiple cells
        self.north_cell = None
        self.east_cell = None
        self.south_cell = None
        self.west_cell = None

    # This method will setup the properties from the constructor with their actual values
    def initialize_cell(self):
        # The linked nodes are set to variables based on their position in the linked maze's node array
        self.top_right_node = self.maze.nodes[self.x_position + 1][self.y_position + 1]
        self.top_left_node = self.maze.nodes[self.x_position][self.y_position + 1]
        self.bottom_left_node = self.maze.nodes[self.x_position][self.y_position]
        self.bottom_right_node = self.maze.nodes[self.x_position + 1][self.y_position]

        # Neighbouring cells are linked in a similar way, and also checked to ensure cells that do not exist are not being accessed.
        self.north_cell = self.maze.cells[self.x_position][self.y_position + 1] if self.y_position + 1 < self.maze.height else None
        self.east_cell = self.maze.cells[self.x_position + 1][self.y_position] if self.x_position + 1 < self.maze.width else None
        self.south_cell = self.maze.cells[self.x_position][self.y_position - 1] if self.y_position - 1 >= 0 else None
        self.west_cell = self.maze.cells[self.x_position - 1][self.y_position] if self.x_position - 1 >= 0 else None

    # From the tremaux algorithm, when the robot drives through a wall, it is visited
    # This method will update the nodes linked to the cell so that they will return the correct value when checked
    def visit_wall(self, wall):
        # The below if statements will select the appropriate linked nodes for the given wall in the parameters and update how many times they have been visited
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

    # This method will take the wall given in the parameters and return how many times that wall has been visited according to the tremaux algorithm
    def check_visited(self, wall):
        if wall == Walls.North:
            return self.top_right_node.west_visited
        if wall == Walls.East:
            return self.top_right_node.south_visited
        if wall == Walls.South:
            return self.bottom_right_node.west_visited
        if wall == Walls.West:
            return self.top_left_node.south_visited
        # The returned value is gotten from the linked node so that even if another cell was the one which set the amount of times visited, the value returned will still be correct

    # When a cells wall state is inferred from the data the maze contains this function is called
    def force_wall(self, wall, amount=2):
        # The amount parameter sets how many times that cell should have been visited according to the tremaux algorithm
        for visit in range(amount):
            self.visit_wall(wall)

        # The following if statements then update the correct wall and set the nodes forced variable so it can be returned correctly when checking if a cell has been forced
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

    # To see if a cell wall's state has been assigned from context, this function checks the appropriate linked nodes for their forced state and return the value
    def check_forced(self, wall):
        if wall == Walls.North:
            return self.top_right_node.west_forced
        if wall == Walls.East:
            return self.top_right_node.south_forced
        if wall == Walls.South:
            return self.bottom_right_node.west_forced
        if wall == Walls.West:
            return self.top_left_node.south_forced

    # This method updates the cells north wall to the given state and sets its value to known
    def update_north(self, state):
        # Nodes are used so that changes are synced among different cells
        self.top_right_node.west_known = True
        self.top_left_node.east_known = True
        if state:
            self.top_right_node.west_node = self.top_left_node
            self.top_left_node.east_node = self.top_right_node

    # This method updates the cells east wall to the given state and sets its value to known
    def update_east(self, state):
        # Nodes are used so that changes are synced among different cells
        self.top_right_node.south_known = True
        self.bottom_right_node.north_known = True
        if state:
            self.top_right_node.south_node = self.bottom_right_node
            self.bottom_right_node.north_node = self.top_right_node

    # This method updates the cells south wall to the given state and sets its value to known
    def update_south(self, state):
        # Nodes are used so that changes are synced among different cells
        self.bottom_right_node.west_known = True
        self.bottom_left_node.east_known = True
        if state:
            self.bottom_right_node.west_node = self.bottom_left_node
            self.bottom_left_node.east_node = self.bottom_right_node

    # This method updates the cells west wall to the given state and sets its value to known
    def update_west(self, state):
        # Nodes are used so that changes are synced among different cells
        self.top_left_node.south_known = True
        self.bottom_left_node.north_known = True
        if state:
            self.top_left_node.south_node = self.bottom_left_node
            self.bottom_left_node.north_node = self.top_left_node

    # Checking if a wall in a cell is known can be done with this function
    def wall_known(self, wall):
        # The if statements below will check if the walls appropriate nodes have known values and if so, returns True to the calling function
        if wall == Walls.North:
            return self.top_right_node.west_known and self.top_left_node.east_known
        if wall == Walls.East:
            return self.top_right_node.south_known and self.bottom_right_node.north_known
        if wall == Walls.South:
            return self.bottom_right_node.west_known and self.bottom_left_node.east_known
        if wall == Walls.West:
            return self.top_left_node.south_known and self.bottom_left_node.north_known

    # To see if all of the walls in a cell are known, this function checks if each wall is known and if so returns True
    def fully_known(self):
        top_right_known = self.top_right_node.west_known and self.top_right_node.south_known
        top_left_known = self.top_left_node.east_known and self.top_left_node.south_known
        bottom_right_known = self.bottom_right_node.north_known and self.bottom_right_node.west_known
        bottom_left_known = self.bottom_left_node.east_known and self.bottom_left_node.north_known

        return top_right_known and top_left_known and bottom_right_known and bottom_left_known

    # Check wall will return if a wall is present in a cell, regardless of if that wall's state is actually known
    def check_wall(self, wall):
        if wall == Walls.North: return self.top_right_node.west_node is not None and self.top_left_node.east_node is not None
        if wall == Walls.East: return self.top_right_node.south_node is not None and self.bottom_right_node.north_node is not None
        if wall == Walls.South: return self.bottom_right_node.west_node is not None and self.bottom_left_node.east_node is not None
        if wall == Walls.West: return self.top_left_node.south_node is not None and self.bottom_left_node.north_node is not None

    # This method will return the unicode character that represents the state of a given wall in the cell
    def get_unicode_char(self, wall):
        # The check wall method is used and a unicode character is returned regardless of if the value is known or not
        # This causes unknown values to return spaces and thus we can use the maze's print function through the exploration phase to see the robots progress
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


# The maze is the overall structure of cells and what stores the representation of the real world maze.
class Maze:
    # The maze constructor creates the variables that will be used to store the nodes and cells inside of the made
    def __init__(self, width, height):
        # The width and height will later be used in the initialize method for setting up the nested lists
        self.width = width
        self.height = height

        self.cells = []
        self.nodes = []

    # Initializing the maze with this method sets up the nested lists that hold the structure of the cells
    # It also sets up the nodes (corners) so the cells can be correctly initialized also
    def initialize_maze(self):
        # This creates sets of cell arrays which correspond to rows in the 'grid' of the maze
        for x_pos in range(self.width):
            self.cells.append([])
            for y_pos in range(self.height):
                # This creates a new cell at the given x, y position and stores it in the data structure
                self.cells[x_pos].append(Cell(x_pos, y_pos, self))

        # Similarly this creates the node arrays which store the nodes in the data structure
        for x_pos in range(self.width + 1):
            self.nodes.append([])
            for y_pos in range(self.height + 1):
                # Nodes are created and added to the list, they are given no information about their position as it is managed by the cells and maze
                self.nodes[x_pos].append(Node())

        # Following the setup of the cell and node lists, the cells are looped through and initialized themselves.
        for cell_array in self.cells:
            for cell in cell_array:
                cell.initialize_cell()

    # update_cell is called for a cell at the give (x_pos, y_pos) location in the maze
    # It updates the wall set in the method's parameters to the given state, with True meaning a wall is present
    def update_cell(self, x_pos, y_pos, wall, state):
        # The following checks ensures no index outside of the bounds of the cell array will be accessed
        if x_pos - 1 > len(self.cells) or y_pos - 1 > len(self.cells[x_pos]):
            return
        if x_pos < 0 or y_pos < 0:
            return

        # This calls the appropriate update method on the given cell depending on which wall is being updated
        # It also calls an update method on the cell with the common wall if that cell exists
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

    # This method can check a given cell for having three present walls, and if this is the case
    # For extra speed we can assume that s a cell must be accessible from at least one side
    # therefore if there is three walls present, we can infer that the last edge is going to not be present
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

    # Fix Actually known corners checks every cell in the maze if it can extrapolate any edges
    def fix_actually_known_corners(self):
        amount_changed = 0
        # the for loop below checks every cell in every cell array in the maze to try extrapolate edges in that cell
        for cell_arr in self.cells:
            for cell in cell_arr:
                amount_changed += self.extrapolate_edges(cell)
        # Ths amount of cells that have been changed is returned so the function can be run again using the new data it has just generated
        return amount_changed

    # This method will return if a value for the state of every wall in a cell is known
    def all_cells_known(self):
        for cell_array in self.cells:
            for cell in cell_array:
                # This method uses the cells fully_known method to check if that cell is fully known
                cell_fully_known = cell.fully_known()
                # When the cell is not known, the function returns as it does not need to check any more cells
                if not cell_fully_known:
                    return False
        return True

    # This pathfinding method uses a breath first algorithm to pathfind from the start position (x_start, y_start) in the parameters
    # to the end position (x_end, y_end) specified in the parameters
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

    # Print plain will print the mazes current interpretation of the maze as it has been traversed. It prints from top to bottom using the characters returned by the cells and nodes themselves
    def print_plain(self):
        # The maze firstly prints the top row of walls, as there is no cell further up and therefore a different wall must be used than the south wall which the other cells use
        for x_pos in range(self.width):
            brain.print(self.nodes[x_pos][self.height].get_unicode_char())
            decremented_height = self.height - 1
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
        brain.print(self.nodes[self.width][self.height].get_unicode_char())

        # Then the rest of the cells are printed from top to bottom, using the unicode characters that the cells return
        for y_pos in reversed(range(self.height)):
            brain.new_line()
            for x_pos in range(self.width):
                brain.print(self.cells[x_pos][y_pos].get_unicode_char(Walls.West))
                brain.print(' ')
                brain.print(' ')
                brain.print(' ')
            decremented_width = self.width - 1
            # here the east wall must be used as there is no other cell further right
            brain.print(self.cells[decremented_width][y_pos].get_unicode_char(Walls.East))

            brain.new_line()
            # Following from printing the left and right walls, the south walls are then printed in a similar fashion
            for x_pos in range(self.width):
                brain.print(self.nodes[x_pos][y_pos].get_unicode_char())
                brain.print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
                brain.print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
                brain.print(self.cells[x_pos][y_pos].get_unicode_char(Walls.South))
            brain.print(self.nodes[self.width][y_pos].get_unicode_char())

    # Print path is essentially a clone of print plain, except for it adds additional characters in the center of cells and walls where the path goes through
    # The path displayed is the one specified in the parameters, and it is shown using the path character also specified
    def print_path(self, path, path_char):
        # Similarly this method starts by printing the north walls, which do not need to use the path as you cannot go through the bounding walls
        for x_pos in range(self.width):
            brain.print(self.nodes[x_pos][self.height].get_unicode_char())
            decremented_height = self.height - 1
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
            brain.print(self.cells[x_pos][decremented_height].get_unicode_char(Walls.North))
        brain.print(self.nodes[self.width][self.height].get_unicode_char())

        # THen the right and left walls are printed
        for y_pos in reversed(range(self.height)):
            brain.new_line()
            for x_pos in range(self.width):
                wall_char = self.cells[x_pos][y_pos].get_unicode_char(Walls.West)
                # These checks dictate if a path character should be used as the wall or cell is in the path
                # Mid in path means that the center of a cell is in the path
                mid_in_path = (x_pos, y_pos) in path
                # Wall in path is for when the path goes through that wall
                wall_in_path = wall_char == ' ' and mid_in_path and (x_pos - 1, y_pos) in path
                brain.print(path_char if wall_in_path else wall_char)
                brain.print(' ')
                brain.print(path_char if mid_in_path else ' ')
                brain.print(' ')
            decremented_width = self.width - 1
            brain.print(self.cells[decremented_width][y_pos].get_unicode_char(Walls.East))

            # finally the bottom walls are printed with another wall_in_path variable which dictates if the path character should be used instead of a space
            brain.new_line()
            for x_pos in range(self.width):
                wall_char = self.cells[x_pos][y_pos].get_unicode_char(Walls.South)
                wall_in_path = wall_char == ' ' and (x_pos, y_pos) in path and (x_pos, y_pos - 1) in path
                brain.print(self.nodes[x_pos][y_pos].get_unicode_char())
                brain.print(wall_char)
                brain.print(path_char if wall_in_path else wall_char)
                brain.print(wall_char)
            brain.print(self.nodes[self.width][y_pos].get_unicode_char())


# The robot object is what manages the state and movement of the robot
class Robot:
    # This constructor sets up all of the robots properties
    def __init__(self, maze, maze_cell_length=250, distance_unit=MM, angle_unit=DEGREES, ):
        # These values set the physical robots properties
        drivetrain.set_drive_velocity(100, PERCENT)
        drivetrain.set_turn_velocity(100, PERCENT)
        pen.move(DOWN)

        # These values set the robot's internal maze to the maze specified in the parameters
        self.maze = maze
        self.maze_cell_length = maze_cell_length

        # These values dictate the units that the robot should use
        self.distance_unit = distance_unit
        self.angle_unit = angle_unit

        # These values are used when checking for a wall being present when looking straight at is, and to the side of it respectively
        self.long_tolerance = 150
        self.short_tolerance = 100
        self.short_turn_offset = 30

    # This method is called to make the robot drive through one square
    # the forward parameter sets which way the robot should drive
    def drive_square(self, forward):
        drive_direction = FORWARD if forward else REVERSE
        drivetrain.drive_for(drive_direction, self.maze_cell_length, self.distance_unit)
        return

    # To get the current position of the robot as x, y co-ordinates, this method is used
    def get_current_cell_location(self):
        x_pos = location.position(X, MM) + 1000
        y_pos = location.position(Y, MM) + 1000

        x_cell = x_pos // self.maze_cell_length
        y_cell = y_pos // self.maze_cell_length

        # the returned x_cell and y_cell numbers are the x and y positions of the robot respectively
        # if the maze was to be thought of as a grid
        return x_cell, y_cell

    # the cell returned by this method is which cell in the maze that the robot is currently located in
    def get_current_cell(self):
        cell_location = self.get_current_cell_location()
        return self.maze.cells[cell_location[0]][cell_location[1]]

    # get_facing_wall returns which wall from the Walls enum that the robot is currently facing
    def get_facing_wall(self):
        heading = drivetrain.heading(self.angle_unit)

        # These cases calculate which wall to return based on which direction the robot is facing
        if heading > 315 or heading < 45:
            return Walls.North
        if 45 <= heading < 135:
            return Walls.East
        if 135 <= heading < 225:
            return Walls.South
        if 225 <= heading < 315:
            return Walls.West

    # This method turns the robot so it faces the wall specified in the parameters
    def turn_to_wall(self, wall):
        self.get_facing_wall()
        # Here we take the modulo of the heading so that it is always positive
        target_wall_heading = (90 * wall) % 360
        drivetrain.turn_to_heading(target_wall_heading, self.angle_unit)
        # The robot also checks in front of it regardless of what action is calling this method
        # This is so it can extract as much information out of each movement because it is facing directly at a wall
        self.check_forward_wall(True)

    # During the maze exploration algorithm, to save time some walls are checked by only turning a small amount
    # the wall specified what wall it should turn to, and clockwise is boolean which is True when you want to approach turning clockwise
    def turn_short_to_wall(self, wall, clockwise):  # clockwise is if you are going clockwise
        # Here we assume the robot will come from the anticlockwise direction
        target_wall_heading = (90 * wall + self.short_turn_offset)
        # The if statement below sets the heading to the correct value if clockwise parameter is True
        if clockwise: target_wall_heading -= 2 * self.short_turn_offset
        target_wall_heading %= 360
        drivetrain.turn_to_heading(target_wall_heading, self.angle_unit)

    # Drive through wall is used when the robot needs to drive through a square at the wall specified
    def drive_through_wall(self, wall):
        facing_wall = self.get_facing_wall()
        # To decide if the robot should travel forward or reverse to increase speed, the wall is checked for if it is in front, or directly behind the robot
        if facing_wall == wall:
            self.turn_to_wall(wall)
            # For each of the different cases, for the direction needed to turn to go through the wall
            # Following making the appropriate turn, the robot drives through a length of the maze grid size using the method below
            self.drive_square(True)
            return
        # This check will see if the wall is not in front or behind the wall
        if wall % 2 != facing_wall % 2:
            self.turn_to_wall(wall)
            self.drive_square(True)
            return
        # If the wall is behind the robot, it squares up the robot to face the facing wall fully, and then reverses
        self.turn_to_wall((wall + 2) % 4)
        self.drive_square(False)

    # The check forward wall is called to check a wall that the robot is looking at
    # It will return True if a wall is present
    # Initially this function checked further away than a single square in front, but due to accuracy issues as the robot was moving
    # testing dictated that it was faster to remove it than slow down the turn speed or wait for a period
    def check_forward_wall(self, full):
        # Firstly details about the robots state are gotten
        current_position = self.get_current_cell_location()
        facing_wall = self.get_facing_wall()
        distance_to_wall = distance.get_distance(self.distance_unit)

        # A tolerance variable is then set depending on if the check if fully facing the wall
        if full:
            tolerance = self.long_tolerance
        else:
            tolerance = self.short_tolerance

        # The wall in front is then checked against the tolerance
        state = distance_to_wall < tolerance
        # The maze is then updated with the new knowledge of the wall
        self.maze.update_cell(current_position[0], current_position[1], facing_wall, state)

        # Following the update of the cell, the robot checks to see if there are any corners who's values it can infer
        # This check must not be done inside the update function itself, as it exceeds the vexcode vr's platform recursion limits for functions
        fixed_corners = -1
        while fixed_corners != 0:
            fixed_corners = self.maze.fix_actually_known_corners()

        # following this the value of the wall just checked is returned. This is checked rather than returned from the state as the wall may have been overridden with static data
        # This is the case with the walls at the south of the starting point and the north of the ending point
        return self.get_current_cell().check_wall(facing_wall)

    # This method checks if a wall is present when the robot is only partially facing the wall
    def check_short_forward(self):
        # Firstly details about the robots state are gotten
        current_position = self.get_current_cell_location()
        facing_wall = self.get_facing_wall()
        distance_to_wall = distance.get_distance(self.distance_unit)

        # The wall in front is then checked against the short wall tolerance property set in the constructor
        state = distance_to_wall < self.short_tolerance
        # The maze is then updated with the new knowledge of the wall
        self.maze.update_cell(current_position[0], current_position[1], facing_wall, state)

        # Following the update of the cell, the robot checks to see if there are any corners who's values it can infer
        # This check must not be done inside the update function itself, as it exceeds the vexcode vr's platform recursion limits for functions
        fixed_corners = -1
        while fixed_corners != 0:
            fixed_corners = self.maze.fix_actually_known_corners()

        # following this the value of the wall just checked is returned. This is checked rather than returned from the state as the wall may have been overridden with static data
        # This is the case with the walls at the south of the starting point and the north of the ending point
        return self.get_current_cell().check_wall(facing_wall)

    def check_junction(self):
        # To check a junction, the current cell is gotten from the get_current_cell method
        current_cell = self.get_current_cell()

        # The enum values of each of the walls is then calculated as integers
        wall_one_direction = int(self.get_facing_wall())
        wall_zero_direction = (wall_one_direction - 1) % 4
        wall_two_direction = (wall_one_direction + 1) % 4
        wall_three_direction = (wall_one_direction + 2) % 4

        # As wall one is defined as the facing wall, we can check its distance manually
        wall_one = self.check_forward_wall(True)

        # Here we check if the wall is known, and if it is the value is saved to the wall_(wall number) variable
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

        # To ensure the smallest amount of turning is used, the following series of if statements are used
        # The first set is all the cases of walls not being known, given the wall to the left (wall_zero) is not known
        if wall_zero is None:
            if wall_three is None:
                self.turn_to_wall(wall_zero_direction)
                wall_zero = self.check_forward_wall(True)
                if wall_two is None:
                    self.turn_to_wall(wall_three_direction)
                    wall_three = self.check_forward_wall(True)
                    self.turn_short_to_wall(wall_two_direction, True)
                    wall_two = self.check_forward_wall(False)
                else:
                    self.turn_short_to_wall(wall_three_direction, False)
                    wall_three = self.check_forward_wall(False)
            elif wall_two is None:
                self.turn_short_to_wall(wall_zero_direction, False)
                wall_zero = self.check_forward_wall(False)
                self.turn_short_to_wall(wall_two_direction, True)
                wall_two = self.check_forward_wall(False)
            else:
                self.turn_short_to_wall(wall_zero_direction, False)
                wall_zero = self.check_forward_wall(False)
        # The next set checks what walls to the right of the robot are present, given the wall to the left is known
        elif wall_two is None:
            if wall_three is None:
                self.turn_to_wall(wall_two_direction)
                wall_two = self.check_forward_wall(True)
                self.turn_short_to_wall(wall_three_direction, True)
                wall_three = self.check_forward_wall(False)
            else:
                self.turn_short_to_wall(wall_two_direction, True)
                wall_two = self.check_forward_wall(False)
        # Even if the left and right walls are known, we may be able to extract more data by checking the wall again as we pass it, as this does not incur a time loss
        elif wall_three is None:
            self.turn_to_wall(wall_two_direction)
            wall_two = self.check_forward_wall(True)
            self.turn_short_to_wall(wall_three_direction, True)
            wall_three = self.check_forward_wall(False)

        # The walls are then sorted by the direction value which corresponds to the Walls enum
        # This ensures that the values returned by this function are in the same order every time
        directions_sorted = []
        # Append is used here as creating this list as a list literal would leave a very long line
        directions_sorted.append((wall_zero_direction, wall_zero))
        directions_sorted.append((wall_one_direction, wall_one))
        directions_sorted.append((wall_two_direction, wall_two))
        directions_sorted.append((wall_three_direction, wall_three))
        directions_sorted.sort()

        # As the directions_sorted have been sorted by their direction, only the states of the walls needs to be returned
        result = []
        # the for loop below takes each wall state and adds it to the result list to be returned
        for junction_direction in directions_sorted: result.append(junction_direction[1])
        return result

    def tremaux_algorithm(self):
        # The algorithm will loop while it is not finished
        finished = False
        while not finished:

            # Every loop it will check if it can infer any edges
            fixed_corners = -1
            while fixed_corners != 0:
                fixed_corners = self.maze.fix_actually_known_corners()

            # it then updated the finiched variable and returns if it is finished
            finished = self.maze.all_cells_known()
            if finished: return

            # The current maze interpretation is then printed as a nice visual progress display
            brain.clear()
            self.maze.print_plain()

            # variables are then created about the current state of the robot
            current_cell = self.get_current_cell()
            facing_wall = self.get_facing_wall()

            # The paths returned by the junction check are then checks for how many times they have been visited
            possible_paths = []
            junction_states = self.check_junction()
            for index in range(len(junction_states)):
                if not junction_states[index]:
                    times_visited = current_cell.check_visited(index)
                    possible_paths.append((times_visited, index))

            # They are then sorted
            possible_paths.sort()
            next_direction = None

            # The next direction is chosen giving priority to easier to reach paths (less turning)
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

            # The path is then marked as visited and then the robot drives through it
            current_cell.visit_wall(next_direction)
            self.drive_through_wall(next_direction)


# The static map data below sets given values for states of walls in the maze
def set_static_map_data(maze):
    # This states that we want to use the global competition mode constant in this function
    global COMPETITION_MODE

    # here we must set the data for the walls at the start and end as the down eye color sensor appears not to work on certain browsers
    # The alternative to this is to use the down eye to check for green or red and set the wall appropriately, but this is safer given the context
    maze.update_cell(4, 0, Walls.South, True)
    maze.update_cell(3, 7, Walls.North, True)

    # The competition mode setting relies on the knowledge that the outsides of the maze will always have walls
    # The calls to update the maze below force this condition so that the robot doesnt need to check if walls are present at the edges of the maze
    # and thus saves time from turning

    # The robot will function without this and it can be disabled at the top of the file
    if COMPETITION_MODE:
        # Sets the bottom walls to be present
        maze.update_cell(0, 0, Walls.South, True)
        maze.update_cell(1, 0, Walls.South, True)
        maze.update_cell(2, 0, Walls.South, True)
        maze.update_cell(3, 0, Walls.South, True)
        maze.update_cell(5, 0, Walls.South, True)
        maze.update_cell(6, 0, Walls.South, True)
        maze.update_cell(7, 0, Walls.South, True)

        # Sets the top walls to be present
        maze.update_cell(0, 7, Walls.North, True)
        maze.update_cell(1, 7, Walls.North, True)
        maze.update_cell(2, 7, Walls.North, True)
        maze.update_cell(3, 7, Walls.North, True)
        maze.update_cell(4, 7, Walls.North, True)
        maze.update_cell(5, 7, Walls.North, True)
        maze.update_cell(6, 7, Walls.North, True)
        maze.update_cell(7, 7, Walls.North, True)

        # Sets the left walls to be present
        maze.update_cell(0, 0, Walls.West, True)
        maze.update_cell(0, 1, Walls.West, True)
        maze.update_cell(0, 2, Walls.West, True)
        maze.update_cell(0, 3, Walls.West, True)
        maze.update_cell(0, 4, Walls.West, True)
        maze.update_cell(0, 5, Walls.West, True)
        maze.update_cell(0, 6, Walls.West, True)
        maze.update_cell(0, 7, Walls.West, True)

        # Sets the right walls to be present
        maze.update_cell(7, 0, Walls.East, True)
        maze.update_cell(7, 1, Walls.East, True)
        maze.update_cell(7, 2, Walls.East, True)
        maze.update_cell(7, 3, Walls.East, True)
        maze.update_cell(7, 4, Walls.East, True)
        maze.update_cell(7, 5, Walls.East, True)
        maze.update_cell(7, 6, Walls.East, True)
        maze.update_cell(7, 7, Walls.East, True)


# The main function is used to start and stop the entire process. It also controls everything in the environment such as setting up the maze, robot and printing the maze when mapping is complete
def main():
    # Here we create the maze object, with the size of the maze
    maze = Maze(8, 8)

    # Here we initialize the maze as the method cannot be called in the constructor of the maze itself
    maze.initialize_maze()

    # Static data for the map is set for the maze created above. The amount of static data depends on the use of the COMPETITION_MODE setting
    # by default it will just use the start and end points for every map in the vexcode platform
    set_static_map_data(maze)

    # The robot is then created using the maze to base itself off of
    robot = Robot(maze)
    # The robot is then instructed to use the Tremaux algorithm to map the maze
    robot.tremaux_algorithm()

    # Once mapping is complete we clear the console then print the maze in a plain format
    brain.clear()
    maze.print_plain()

    # The maze then uses a breath first algorithm to generate an optimal path through the internal representation of the maze
    path = maze.pathfind_breath_first(4, 0, 3, 7)

    # This path is then displayed on the printout of the maze using '•' as a marker for the path
    brain.new_line()
    maze.print_path(path, '•')

    # As the maze mapping and printout are complete, we then stop the project
    brain_print_line("Program Complete")
    stop_project()


# This function is used to print something on a new line rather than call brain.newline and brain.print every time
def brain_print_line(obj):
    brain.new_line()
    brain.print(obj)


# VR threads — Do not delete
vr_thread(main())

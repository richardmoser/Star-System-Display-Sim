"""
This file contains functions that are used in multiple files. Hopefully it will make the code more readable.
"""

import os
import random
import math
import pygame

"""
do not move this block until you are smart enough to do so
"""
# this block must be above the pygame.init() line
if os.path.exists("last_window_position.txt"):
    with open("last_window_position.txt", "r") as f:
        window_position = f.read()
else:
    #create the file and write the default window position to it
    with open("last_window_position.txt", "w") as f:
        f.write("(0, 0)")
print(f"window position: {window_position} read from file")
x = int(window_position.split(",")[0].split("(")[1])
y = int(window_position.split(",")[1].split(")")[0])
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x,y)

# initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))

COLOR_WHITE = (255, 255, 255)
COLOR_UNIVERSE = (36, 36, 36)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
# COLOR_PALE_BLUE = (0, 191, 255)
# COLOR_PALE_BLUE = (0, 255, 255)
COLOR_TAC_GREEN = (89, 255, 66)

# TODO: figure out how to make WIDTH and HEIGHT accessible to all files. orbital_map.py needs them as do functions in
#  library.py below.
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)


# set the title of the window
pygame.display.set_caption("system_map")

# create a clock
clock = pygame.time.Clock()
"""
end of block
"""

def configure():
    # if config.txt exists, read it and set the variables accordingly, otherwise set the variables to default values
    # config.txt should contain the following variables: screen_size, COLOR_UNIVERSE

    if os.path.exists("config.txt"):
        with open("config.txt", "r") as f:
            config = f.read()
        screen_size = config.split("screen_size:")[1].split("\n")[0].strip()
        color_universe = config.split("COLOR_UNIVERSE:")[1].split("\n")[0].strip()
        # print(f"screen_size: {screen_size}")
        # print(f"color_universe: {color_universe}")

    else:
        screen_size = (800, 800)
        color_universe = "COLOR_UNIVERSE"


def plot_circle(x, y, r):
    """
    plots a circle
    :param x: x coordinate
    :param y: y coordinate
    :param r: radius
    :return: None
    """
    # draw a circle
    pygame.draw.circle(screen, (255, 255, 255), (x, y), r)

def rand_pt_in_range(r_min, r_max):
    """
    generates a random point whose distance from the origin falls within the
    specified range
    """
    # generate a random distance from the origin
    r = random.randint(r_min, r_max)
    # generate a random angle
    theta = random.uniform(0, 2 * math.pi)
    # calculate the x and y coordinates
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    # calculate the radius
    # radius = math.sqrt(x ** 2 + y ** 2)
    # return the coordinates
    return x, y


def random_radius_distribution(n, rmin, rmax, min_space=60):
    """
    generates a random distribution of radii
    :param n: number of radii to generate
    :param rmin: minimum radius
    :param rmax: maximum radius
    :param min_space: minimum space between radii
    :return: list of radii
    """
    # create an empty list
    radii = []

    radii.append(rmin)
    # loop until the list has n radii
    i = 1
    while len(radii) < n:
        r = random.randint(radii[i - 1] + min_space, radii[i - 1] + rmax)
        #                                   80 + 60, 80 + 200 = 140, 2800
        radii.append(r)
        i += 1

    # return the sorted list
    # radii = sorted(radii)
    return radii


def select_planet(planet_no, planets):
    """
    Draw the corners of a square around the planet
    :param planet_no: the number of the planet which is being selected
    :return: None
    """
    # calculate the x and y coordinates of the planet
    x = planets[planet_no].x
    y = planets[planet_no].y
    # draw the corners of the square
    # pygame.draw.circle(screen, (255, 255, 255), (x - planets[planet_no].radius, y - planets[planet_no].radius), 5)
    # pygame.draw.circle(screen, (255, 255, 255), (x + planets[planet_no].radius, y - planets[planet_no].radius), 5)
    # pygame.draw.circle(screen, (255, 255, 255), (x - planets[planet_no].radius, y + planets[planet_no].radius), 5)
    # pygame.draw.circle(screen, (255, 255, 255), (x + planets[planet_no].radius, y + planets[planet_no].radius), 5)

    # use draw.lines to draw two lines for each corner of the square. The sides should stand off the planet by 10 pixels and the length of the lines should be 30% of the radius

    pygame.draw.lines(screen, (255, 255, 255), False, [(x - planets[planet_no].radius, y - planets[planet_no].radius), (x - planets[planet_no].radius + int(0.3 * planets[planet_no].radius), y - planets[planet_no].radius)], 1)  # the top left corner to the left side of the planet
    pygame.draw.lines(screen, (255, 255, 255), False, [(x - planets[planet_no].radius, y - planets[planet_no].radius), (x - planets[planet_no].radius, y - planets[planet_no].radius + int(0.3 * planets[planet_no].radius))], 1)  # the top left corner to the top side of the planet

    pygame.draw.lines(screen, (255, 255, 255), False, [(x + planets[planet_no].radius, y - planets[planet_no].radius), (x + planets[planet_no].radius - int(0.3 * planets[planet_no].radius), y - planets[planet_no].radius)], 1)  # the top right corner to the right side of the planet
    pygame.draw.lines(screen, (255, 255, 255), False, [(x + planets[planet_no].radius, y - planets[planet_no].radius), (x + planets[planet_no].radius, y - planets[planet_no].radius + int(0.3 * planets[planet_no].radius))], 1)  # the top right corner to the top side of the planet

    pygame.draw.lines(screen, (255, 255, 255), False, [(x - planets[planet_no].radius, y + planets[planet_no].radius), (x - planets[planet_no].radius + int(0.3 * planets[planet_no].radius), y + planets[planet_no].radius)], 1)  # the bottom left corner to the left side of the planet
    pygame.draw.lines(screen, (255, 255, 255), False, [(x - planets[planet_no].radius, y + planets[planet_no].radius), (x - planets[planet_no].radius, y + planets[planet_no].radius - int(0.3 * planets[planet_no].radius))], 1)  # the bottom left corner to the bottom side of the planet

    pygame.draw.lines(screen, (255, 255, 255), False, [(x + planets[planet_no].radius, y + planets[planet_no].radius), (x + planets[planet_no].radius - int(0.3 * planets[planet_no].radius), y + planets[planet_no].radius)], 1)  # the bottom right corner to the right side of the planet
    pygame.draw.lines(screen, (255, 255, 255), False, [(x + planets[planet_no].radius, y + planets[planet_no].radius), (x + planets[planet_no].radius, y + planets[planet_no].radius - int(0.3 * planets[planet_no].radius))], 1)  # the bottom right corner to the bottom side of the planet



class Planet:
    """
    defines a planet class which will be used to create planets. planets have a
    starting x and y coordinate, a radius, color, orbital_radius, orbital_speed,
    and a name
    """
    SCALE = 1
    def __init__(self, name, radius, orbital_radius, color):
        """
        initializes the planet class
        :param radius: radius
        :param color: color
        :param orbital_speed: orbital speed
        :param name: name
        """

        self.name = name
        self.radius = radius
        self.radius_initial = radius
        self.color = color
        self.orbit = []
        # self.orbital_speed = orbital_speed

        self.theta = random.uniform(0, 2 * math.pi)
        self.orbital_radius = orbital_radius
        self.orbital_radius_initial = orbital_radius
        if str(name) == "0":  # if the planet is the sun
            self.orbital_radius = 0 # set the orbital radius to 0
            self.x = WIDTH / 2 # set the x coordinate to the center of the screen
            self.y = HEIGHT / 2 # set the y coordinate to the center of the screen
            self.orbital_speed = 0 # set the orbital speed to 0
        else: # if the planet is not the sun
            # self.orbital_radius = planet_no * 100
            self.x = self.orbital_radius * math.cos(self.theta) + WIDTH / 2 # calculate the x coordinate
            self.y = self.orbital_radius * math.sin(self.theta) + HEIGHT / 2 # calculate the y coordinate
            self.mass = 4 / 3 * math.pi * (self.radius ** 3) # calculate the mass
            self.orbital_speed = math.sqrt(5 * self.mass / self.orbital_radius ** 3) # calculate the orbital speed


    def draw(self, window, show_name, move_x, move_y, line_to_sun, text_color=COLOR_WHITE):
        x_posit = self.x
        y_posit = self.y
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_posit, y_posit = point
                updated_points.append((x_posit, y_posit))
            if line_to_sun:
                pygame.draw.lines(window, self.color, False, updated_points, 1)
        # pygame.draw.circle(window, self.color, (x + move_x, y + move_y), self.radius)
        pygame.draw.circle(window, self.color, (x_posit , y_posit), self.radius)
        if show_name:
            text = FONT_2.render(self.name, True, text_color)
            window.blit(text, (x_posit + move_x - text.get_width() / 2, y_posit + move_y - text.get_height() / 2))
        if line_to_sun:
            pygame.draw.line(window, self.color, (x_posit, y_posit), (WIDTH / 2, HEIGHT / 2), 1)


    def update_position(self, move_x, move_y):
        """
        updates the position of the planets. gravity is not taken into account
        :return: None
        """
        # calculate the new x and y coordinates
        if str(self.name) == "0":
            self.x = WIDTH / 2 + move_x
            self.y = HEIGHT / 2 + move_y
            return
        self.x = self.orbital_radius * math.cos(self.theta) + WIDTH / 2 + move_x
        self.y = self.orbital_radius * math.sin(self.theta) + HEIGHT / 2 + move_y
        # add the new coordinates to the orbit list
        self.orbit.append((self.x, self.y))
        # increment theta
        self.theta += self.orbital_speed * 0.002


    def update_radius(self, scale):
        """
        updates the radius of the planet
        :param scale: scale
        :return: None
        """
        self.radius *= scale
        self.orbital_radius *= scale


    def reset_radius(self):
        """
        resets the radius of the planet
        :return: None
        """
        self.radius = self.radius_initial
        self.orbital_radius = self.orbital_radius_initial


    def draw_orbit(self, window, move_x, move_y):
        """
        draws the orbit of the planet
        :param window: window
        :return: None
        """
        x = WIDTH / 2 + move_x
        y = HEIGHT / 2 + move_y
        # pygame.draw.circle(window, self.color, (WIDTH / 2,WIDTH / 2.), self.orbital_radius, 1)
        pygame.draw.circle(window, self.color, (x, y), self.orbital_radius, 1)


class Moon:
    """
    defines a moon class which will be used to create moons. moons have a
    host planet, a radius, color, orbital_radius, orbital_speed,
    and a name
    """

    def __init__(self, host_planet, color, orbital_radius, orbital_speed, name):
        """
        initializes the moon class
        :param host_planet: host planet
        :param color: color
        :param orbital_radius: orbital radius
        :param orbital_speed: orbital speed
        :param name: name
        """
        self.name = name
        self.host_planet = host_planet
        self.radius = random.uniform(self.host_planet.radius * 0.2, self.host_planet.radius * 0.4)
        self.radius_initial = self.radius
        self.color = color
        self.orbit = []
        self.orbital_speed = orbital_speed
        self.theta = random.uniform(0, 2 * math.pi)
        # self.orbital_radius = random.randint(host_planet.radius * 1.5, host_planet.radius * 1.9)
        self.orbital_radius = orbital_radius
        self.orbital_radius_initial = self.orbital_radius
        # self.x = orbital_radius * math.cos(self.theta)
        # self.y = orbital_radius * math.sin(self.theta)

        self.x = self.orbital_radius * math.cos(self.theta) + host_planet.x
        self.y = self.orbital_radius * math.sin(self.theta) + host_planet.y

    def draw(self, window, show_name, move_x, move_y, line_to_host=False, text_color=COLOR_WHITE):
        x_posit = self.x
        y_posit = self.y
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_posit, y_posit = point
                updated_points.append((x_posit, y_posit))
            # pygame.draw.lines(window, self.color, False, updated_points, 1)
        pygame.draw.circle(window, self.color, (x_posit, y_posit), self.radius)
        if show_name:
            text = FONT_2.render(self.name, True, text_color)
            window.blit(text, (x_posit + move_x - text.get_width() / 2, y_posit + move_y - text.get_height() / 2))
        if line_to_host:
            pygame.draw.line(window, self.color, (x_posit, y_posit), (self.host_planet.x,
                                                                      self.host_planet.y), 1)

    def update_position(self, move_x, move_y):
        """
        updates the position of the moons. gravity is not taken into account
        :return: None
        """
        # calculate the new x and y coordinates
        self.x = self.orbital_radius * math.cos(self.theta) + self.host_planet.x
        self.y = self.orbital_radius * math.sin(self.theta) + self.host_planet.y
        # add the new coordinates to the orbit list
        self.orbit.append((self.x, self.y))
        # increment theta
        self.theta += self.orbital_speed * 0.0001

    def update_radius(self, scale):
        """
        updates the radius of the moon
        :param scale: scale
        :return: None
        """
        self.radius *= scale
        self.orbital_radius *= scale


    def reset_radius(self):
        """
        resets the radius of the moon
        :return: None
        """
        self.radius = self.radius_initial
        self.orbital_radius = self.orbital_radius_initial


    def draw_orbit(self, window):
        """
        draws the orbit of the planet
        :param window: window
        :return: None
        """
        pygame.draw.circle(window, self.color, (self.host_planet.x, self.host_planet.y), self.orbital_radius, 1)
        # pygame.draw.circle(screen, (255, 255, 255), (0,0), self.orbital_radius)
        # plot_circle(0,0, 30)ddddd

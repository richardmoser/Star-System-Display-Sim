"""
Author: Richard Moser
Date Created: 21Sep23
Version: 0.1
Purpose: generate a star system map with planets, moons, and other objects.
My plan is to use this in an MFD or readout display for a scifi control panel but
it should be adaptable to other uses.
Sources: based on zerot69's Solar System Simulation repo on github. Their
Planet class was used as a template for my Planet and Moon classes. I will likely
forget to update this, so I may have incorporated other functions from Solar
System Simulation at the time of reading.
His app is a colorful recreation of our solar system with a different purpose
and feature set than this one, so make sure to check it out!
https://github.codm/zerot69/Solar-System-Simulation
"""

import pygame
import math
import random
import os

x = 1
y = 31
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x,y)
# initialize pygame
pygame.init()
# set the size of the window
screen = pygame.display.set_mode((800, 800))
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

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

FONT_1 = pygame.font.SysFont("Trebuchet MS", 21)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 16)
# set the title of the window
pygame.display.set_caption("system_map")

# create a clock
clock = pygame.time.Clock()


class Planet:
    """
    defines a planet class which will be used to create planets. planets have a
    starting x and y coordinate, a radius, color, orbital_radius, orbital_speed,
    and a name
    """

    def __init__(self, name, radius, orbital_radius, color, orbital_speed):
        """
        initializes the planet class
        :param radius: radius
        :param color: color
        :param orbital_speed: orbital speed
        :param name: name
        """
        self.name = name
        self.radius = radius
        self.color = color
        self.orbit = []
        self.orbital_speed = orbital_speed
        self.theta = random.uniform(0, 2 * math.pi)
        self.orbital_radius = orbital_radius
        if str(name) == "0":
            self.orbital_radius = 0
            self.x = 400 #WIDTH / 2
            self.y = 400 #HEIGHT / 2
        else:
        #     min_radius = ((planet_no ** 1.2) * 100)
        #     max_radius = (((planet_no + 1) ** 1.1) - ((planet_no + 1) * .9) ** 1.1) * 100
        #     if planet_no == 1:
        #         min_radius += 50
        #     # self.orbital_radius = random.uniform(min_radius, max_radius)
            # self.orbital_radius = planet_no * 100
            self.x = self.orbital_radius * math.cos(self.theta) + WIDTH / 2
            self.y = self.orbital_radius * math.sin(self.theta) + HEIGHT / 2
        # print(f"planet {self.name} orbital radius: {self.orbital_radius}")
        # print(f"planet {self.name} x: {self.x}")
        # print(f"planet {self.name} y: {self.y}")
        # print("")


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


    def update_position(self):
        """
        updates the position of the planets. gravity is not taken into account
        :return: None
        """
        # calculate the new x and y coordinates
        if str(self.name) == "0":
            return
        self.x = self.orbital_radius * math.cos(self.theta) + WIDTH / 2
        self.y = self.orbital_radius * math.sin(self.theta) + HEIGHT / 2
        # add the new coordinates to the orbit list
        self.orbit.append((self.x, self.y))
        # increment theta
        self.theta += self.orbital_speed * 0.0001

    def draw_orbit(self, window):
        """
        draws the orbit of the planet
        :param window: window
        :return: None
        """
        pygame.draw.circle(window, self.color, (WIDTH / 2,WIDTH / 2.), self.orbital_radius, 1)
        # pygame.draw.circle(screen, (255, 255, 255), (0,0), self.orbital_radius)
        # plot_circle(0,0, 30)

class Moon:
    """
    defines a moon class which will be used to create moons. moons have a
    host planet, a radius, color, orbital_radius, orbital_speed,
    and a name
    """

    def __init__(self, host_planet, radius, color, orbital_radius, orbital_speed, name):
        """
        initializes the moon class
        :param host_planet: host planet
        :param radius: radius
        :param color: color
        :param orbital_radius: orbital radius
        :param orbital_speed: orbital speed
        :param name: name
        """
        self.name = name
        self.host_planet = host_planet
        # self.radius = radius
        # while self.radius > self.host_planet.radius:
        # TODO: either delete this and remove the radius parameter or fix it
        self.radius = random.randint(1, int(self.host_planet.radius * 0.5))
        self.color = color
        self.orbit = []
        self.orbital_speed = orbital_speed
        self.theta = random.uniform(0, 2 * math.pi)
        # self.orbital_radius = random.randint(host_planet.radius * 1.5, host_planet.radius * 1.9)
        self.orbital_radius = orbital_radius
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
            pygame.draw.line(window, self.color, (x_posit, y_posit), (self.host_planet.x, self.host_planet.y), 1)

    def update_position(self):
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

    def draw_orbit(self, window):
        """
        draws the orbit of the planet
        :param window: window
        :return: None
        """
        pygame.draw.circle(window, self.color, (self.host_planet.x, self.host_planet.y), self.orbital_radius, 1)
        # pygame.draw.circle(screen, (255, 255, 255), (0,0), self.orbital_radius)
        # plot_circle(0,0, 30)

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


def main():
    system = "Epsilon Eridani"
    planets = []
    moons = []
    print_system = True
    print_planets = False
    print_moons = False
    num_planets = 6
    rmin = (WIDTH / 2  * 0.12)
    rmax = (WIDTH / 2 * 0.15)
    min_space = (WIDTH / 2 * 0.1)
    print(f"rmin: {rmin}, rmax: {rmax}, min_space: {min_space}")
    orbit_radii = random_radius_distribution(num_planets, rmin, rmax, min_space)
    max_moons_inner = 2
    max_moons_outer = 5

    # make the sun
    sun = Planet(0, 25, 0, COLOR_TAC_GREEN, 0)
    # loop through the number of planets to make
    for i in range(num_planets):
        # make a planet
        if i < 2: # if i is a very inner planet
            planets.append(Planet(f" {i + 1}", random.randint(2, 10), orbit_radii[i], COLOR_TAC_GREEN, random.randint(2, 6)))
            num_moons = random.randint(0, 1)
            for j in range(num_moons):
                # make a moon
                moons.append(Moon(planets[i], random.randint(3, 4), COLOR_TAC_GREEN, random.randint(planets[i].radius + 5, planets[i].radius +20), random.randint(5, 15), f"M{j + 1}"))
        elif 2 <= i < 4: # if i is an inner planet
            planets.append(Planet(f" {i + 1}", random.randint(2, 20), orbit_radii[i], COLOR_TAC_GREEN, random.randint(2, 6)))
            num_moons = random.randint(0, max_moons_inner)
            for j in range(num_moons):
                # make a moon
                moons.append(Moon(planets[i], random.randint(1, 3), COLOR_TAC_GREEN, random.randint(planets[i].radius + 5, planets[i].radius +20), random.randint(5, 15), f"M{j + 1}"))
        else: # if i is an outer planet
            planets.append(Planet(f" {i + 1}", random.randint(6, 12), orbit_radii[i], COLOR_TAC_GREEN, random.randint(2, 6)))
            num_moons = random.randint(0, max_moons_outer)
            for j in range(num_moons):
                moons.append(Moon(planets[i], random.randint(2, 3), COLOR_TAC_GREEN, random.randint(planets[i].radius + 7, planets[i].radius +25), random.randint(5, 15), f"M{j + 1}"))
        print(f"Planet {i}, radius: {planets[i].radius} orbital radius: {orbit_radii[i]}, num moons: {num_moons}")
    # set the variable running to True
    running = True

    while running:
        # for every event in pygame
        for event in pygame.event.get():
            # if the event is quit
            if event.type == pygame.QUIT:
                # set running to False
                running = False
        # fill the screen with black
        screen.fill((0, 0, 0))

        # draw the planets
        sun.draw(screen, print_planets, 0, 0, False, COLOR_TAC_GREEN)
        for planet in planets:
            planet.draw_orbit(screen)
            planet.draw(screen, print_planets, 0, planet.radius + 10, False, COLOR_TAC_GREEN)
        for moon in moons:
            moon.draw_orbit(screen)
            moon.draw(screen, print_moons, 0, moon.radius + 10, False, COLOR_TAC_GREEN)
        # print the system name at the top of the screen
        if print_system:
            text = FONT_1.render(system, True, COLOR_TAC_GREEN)
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))

        for planet in planets:
            planet.update_position()
        for moon in moons:
            moon.update_position()

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 10
        # if keys[pygame.K_LEFT] or mouse_x == 0:
        #     move_x += distance
        # if keys[pygame.K_RIGHT] or mouse_x == window_w - 1:
        #     move_x -= distance
        # if keys[pygame.K_UP] or mouse_y == 0:
        #     move_y += distance
        # if keys[pygame.K_DOWN] or mouse_y == window_h - 1:
            # print(sun.x, sun.y)

        # update the display
        pygame.display.update()
        # set the fps to 60
        clock.tick(60)


if __name__ == '__main__':
    main()


"""Functionality"""
# TODO: make moons a subclass of planets
# TODO: make a method of the planet class to add moons using
    # the same random distribution function as the planets
    # moon radius should be a fraction of the planet radius
    # moon orbital radius may need to be spaced relative to the moon radius
# TODO: make orbital velocity a function of orbital radius

# TODO: set autoscale for orbits
# TODO: add zoom in and out feature from sol_map code
    # when zoomed to a certain level, show some stats or something
# TODO: add some kind of auto roam feature to move around the system,
    # zoom in and out, and
# TODO: set a random list of system names

# TODO: add a class for vessels
# TODO: set a random list of names
# TODO: set vessels to come in system and orbit planets
# TODO: set a class for autofactories, mines, etc
    # these can be square markers
# TODO: add a tooltip with text and a line to the object
# TODO: add mouseover information for celestial bodies and objects
# TODO: add a legend/readout for the system
# TODO: add system statistics to the readout

# TODO: set up predefined systems
# TODO: set up a list of ship names
# TODO: set jump warnings for ships
    # set to t seconds before arrival, find x(t) and y(t) for planet as initial orbit
    # position of the ship

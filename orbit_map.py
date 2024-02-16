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
from pygame._sdl2 import Window

from library import *


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
print(f"x: {x}")
print(f"y: {y}")
print("")
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (x, y)
# set the window position to x, y


def main():
    default_scale = 1
    # window_position_recall()
    # screen, FONT_1, FONT_2, clock, screen_size, color_universe = configure()
    move_x = 0
    move_y = 0
    system = "Epsilon Eridani"
    planets = []
    moons = []
    pause = False
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
    selected_planet = None
    selected_counter = 0
    debounce_timer = 0
    zoom_planet = False
    scale_changed = False
    scale = default_scale

    # loop through the number of planets to make
    for i in range(num_planets):
        # make a planet
        if i == 0: # if i is the sun
            planets.append(Planet(0, 25, 0, COLOR_TAC_GREEN))
            # set number of moons to 0
            num_moons = 0

        elif 0 < i < 2: # if i is a very inner planet
            planets.append(Planet(f" {i + 1}", random.randint(2, 10), orbit_radii[i], COLOR_TAC_GREEN))
            num_moons = random.randint(0, 1)
            for j in range(num_moons):
                # make a moon
                moons.append(
                    Moon(planets[i], COLOR_TAC_GREEN, random.randint(planets[i].radius + 5, planets[i].radius + 20),
                         random.randint(5, 15), f"M{j + 1}"))
        elif 2 <= i < 4: # if i is an inner planet
            planets.append(Planet(f" {i + 1}", random.randint(2, 20), orbit_radii[i], COLOR_TAC_GREEN))
            num_moons = random.randint(0, max_moons_inner)
            for j in range(num_moons):
                # make a moon
                moons.append(
                    Moon(planets[i], COLOR_TAC_GREEN, random.randint(planets[i].radius + 5, planets[i].radius + 20),
                         random.randint(5, 15), f"M{j + 1}"))
        else: # if i is an outer planet
            planets.append(Planet(f" {i + 1}", random.randint(6, 12), orbit_radii[i], COLOR_TAC_GREEN))
            num_moons = random.randint(0, max_moons_outer)
            for j in range(num_moons):
                moons.append(
                    Moon(planets[i], COLOR_TAC_GREEN, random.randint(planets[i].radius + 7, planets[i].radius + 25),
                         random.randint(5, 15), f"M{j + 1}"))
        print(f"Planet {i}, radius: {planets[i].radius} orbital radius: {orbit_radii[i]}, num moons: {num_moons}")
    # set the variable running to True
    running = True

    window = Window.from_display_module()
    print(window.position)



    while running:
        clock.tick(60)

        # for every event in pygame
        for event in pygame.event.get():
            # if the event is quit
            if event.type == pygame.QUIT:
                # save window position to file
                with open("last_window_position.txt", "w") as f:
                    f.write(f"{window.position}")
                print(f"window position: {window.position} saved to file")
                # set running to False
                running = False
            # zoom in and out with the mouse wheel or the plus and minus keys
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_KP_MINUS) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 5):
                scale -= 0.25
                scale_changed = True
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_KP_PLUS) or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 4):
                scale += 0.25
                scale_changed = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
        # fill the screen with black
        screen.fill((0, 0, 0))

        if scale_changed:
            for planet in planets:
                planet.update_radius(scale)
            for moon in moons:
                moon.update_radius(scale)
            scale_changed = False

        if not pause:
            for planet in planets:
                planet.translate_body(move_x, move_y)
            for moon in moons:
                moon.translate_body(move_x, move_y)

        # draw the planets
        for planet in planets:
            planet.draw_orbit(screen, move_x, move_y)
            planet.draw(screen, print_planets, 0, planet.radius + 10, False, COLOR_TAC_GREEN)
            if selected_planet is not None:
                if planet == planets[selected_planet]:
                    # call the select_planet method to draw the selected planet for 30 frames and then do not draw it for 30 frames
                    selected_counter += 1
                    if selected_counter < 30:
                        select_planet(selected_planet, planets)
                    if selected_counter >= 60:
                        selected_counter = 0


        for moon in moons:
            moon.draw_orbit(screen)
            moon.draw(screen, print_moons, 0, moon.radius + 10, False, COLOR_TAC_GREEN)
        # print the system name at the top of the screen
        if print_system:
            text = FONT_1.render(system, True, COLOR_TAC_GREEN)
            screen.blit(text, (WIDTH / 2 - text.get_width() / 2, 10))



        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        window_w, window_h = pygame.display.get_surface().get_size()
        distance = 5
        # if the escape key is pressed, set running to False
        if keys[pygame.K_ESCAPE]:
            running = False
        if keys[pygame.K_LEFT]:
            move_x += distance
            window = Window.from_display_module()
        if keys[pygame.K_RIGHT]:
            move_x -= distance
            window = Window.from_display_module()
        if keys[pygame.K_UP]:
            move_y += distance
            window = Window.from_display_module()
        if keys[pygame.K_DOWN]:
            move_y -= distance
            window = Window.from_display_module()
        # if the c key is pressed, center the system
        if keys[pygame.K_c]:
            move_x = 0
            move_y = 0
        # if the z key is pressed, reset the zoom
        if keys[pygame.K_z]:
            for planet in planets:
                planet.reset_radius()
            for moon in moons:
                moon.reset_radius()
        # if the s key is pressed, toggle the system name
        if keys[pygame.K_s]:
            print_system = not print_system
        # TODO: troubleshoot debounce on selection
        # if the a key is pressed, decrement the selected planet. If no planet is selected, select the last planet
        if keys[pygame.K_a]:
            if debounce_timer == 0:
                debounce_timer = 10
                if selected_planet is None:
                    selected_planet = len(planets) - 1
                elif selected_planet == 0:
                    selected_planet = len(planets) - 1
                else:
                    selected_planet -= 1
            # else:
                # debounce_timer -= 1
            just_pressed = debounce_timer == 0
            # if just_pressed:
        # if the d key is pressed, increment the selected planet. If no planet is selected, select the first planet
        if keys[pygame.K_d]:
            if debounce_timer == 0:
                debounce_timer = 10
                if selected_planet is None:
                    selected_planet = 0
                elif selected_planet == len(planets) - 1:
                    selected_planet = 0
                else:
                    selected_planet += 1
            # else:
            #     debounce_timer -= 1
            just_pressed = debounce_timer == 0
        # if the return key is pressed, call zoom_to_planet on the selected planet
        if keys[pygame.K_RETURN]:
            if selected_planet is not None and debounce_timer == 0:
                debounce_timer = 50
                zoom_planet = not zoom_planet
        if keys[pygame.K_p]:
            # print the planet's x, y, and radius and the current screen x, y, and scale
            print(f"Planet {planets[selected_planet].name}, x: {x}, y: {y}, radius: {r}")
            print(f"Screen x: {move_x}, y: {move_y}, scale: {scale}")
            # move_x = window_w


        if zoom_planet:
            # Zooms in to the location of the selected planet 's position over a specified time interval. Zoom in until
            # the planet fills 70 % of the screen. If already zoomed, recenters the planet on the screen.
            x = planets[selected_planet].x
            y = planets[selected_planet].y
            r = planets[selected_planet].radius
            # gradually move the screen to the selected planet using the lerp function
            move_x = lerp(move_x, -x +200, 0.01)
            move_y = lerp(move_y, -y, 0.01)
            # gradually zoom in to the selected planet using the lerp function
            scale = lerp(scale, 3, 0.01)

            scale_changed = True




        debounce_timer -= 1
        if debounce_timer < 0:
            debounce_timer = 0
        # print(planets[0].x, planets[0].y)
        # print(planets[0].SCALE)
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

from math import atan2, pi, sqrt, cos, sin
import random


import strings


class Quadrant():

    def __init__(self):
        self.name = ""
        self.klingons = 0
        self.stars = 0
        self.starbase = False
        self.scanned = False


class SectorType():

    def __init__(self):
        self.empty, self.star, self.klingon, self.enterprise, self.starbase \
            = range(5)

sector_type = SectorType()


class KlingonShip():

    def __init__(self):
        self.sector_x = 0
        self.sector_y = 0
        self.shield_level = 0


class Game():

    def __init__(self):
        self.star_date = 0
        self.time_remaining = 0
        self.energy = 0
        self.klingons = 0
        self.starbases = 0
        self.quadrant_x, self.quadrant_y = 0, 0
        self.sector_x, self.sector_y = 0, 0
        self.shield_level = 0
        self.navigation_damage = 0
        self.short_range_scan_damage = 0
        self.long_range_scan_damage = 0
        self.shield_control_damage = 0
        self.computer_damage = 0
        self.photon_damage = 0
        self.phaser_damage = 0
        self.photon_torpedoes = 0
        self.docked = False
        self.destroyed = False
        self.starbase_x, self.starbase_y = 0, 0
        self.quadrants = [[Quadrant() for _ in range(8)] for _ in range(8)]
        self.sector = [[SectorType() for _ in range(8)] for _ in range(8)]
        self.klingon_ships = []

game = Game()


def run():
    global game
    print_strings(strings.titleStrings)
    while True:
        initialize_game()
        print_mission()
        generate_sector()
        print_strings(strings.command_strings)
        while game.energy > 0 and not game.destroyed and game.klingons > 0 \
                and game.time_remaining > 0:
            command_prompt()
            print_game_status()


def print_game_status():
    global game
    if game.destroyed:
        print "MISSION FAILED: ENTERPRISE DESTROYED!!!"
        print
        print
        print
    elif game.energy == 0:
        print "MISSION FAILED: ENTERPRISE RAN OUT OF ENERGY."
        print
        print
        print
    elif game.klingons == 0:
        print "MISSION ACCOMPLISHED: ALL KLINGON SHIPS DESTROYED. WELL DONE!!!"
        print
        print
        print
    elif game.time_remaining == 0:
        print "MISSION FAILED: ENTERPRISE RAN OUT OF TIME."
        print
        print
        print


def command_prompt():
    command = raw_input("Enter command: ").strip().lower()
    print
    if command == "nav":
        navigation()
    elif command == "srs":
        short_range_scan()
    elif command == "lrs":
        long_range_scan()
    elif command == "pha":
        phaser_controls()
    elif command == "tor":
        torpedo_control()
    elif command == "she":
        shield_controls()
    elif command == "com":
        computer_controls()
    elif command.startswith('qui') or command.startswith('exi'):
        exit()
    else:
        print_strings(strings.command_strings)


def computer_controls():
    global game
    if game.computer_damage > 0:
        print "The main computer is damaged. Repairs are underway."
        print
        return
    print_strings(strings.computer_strings)
    command = raw_input("Enter computer command: ").strip().lower()
    if command == "rec":
        display_galactic_record()
    elif command == "sta":
        display_status()
    elif command == "tor":
        photon_torpedo_calculator()
    elif command == "bas":
        starbase_calculator()
    elif command == "nav":
        navigation_calculator()
    else:
        print
        print "Invalid computer command."
        print
    induce_damage(4)


def compute_direction(x1, y1, x2, y2):
    if x1 == x2:
        if y1 < y2:
            direction = 7
        else:
            direction = 3
    elif y1 == y2:
        if x1 < x2:
            direction = 1
        else:
            direction = 5
    else:
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        angle = atan2(dy, dx)
        if x1 < x2:
            if y1 < y2:
                direction = 9.0 - 4.0 * angle / pi
            else:
                direction = 1.0 + 4.0 * angle / pi
        else:
            if y1 < y2:
                direction = 5.0 + 4.0 * angle / pi
            else:
                direction = 5.0 - 4.0 * angle / pi
    return direction


def navigation_calculator():
    global game
    print
    print "Enterprise located in quadrant [%s,%s]." % (
        game.quadrant_x + 1, game.quadrant_y + 1)
    print
    quad_x = input_double("Enter destination quadrant X (1--8): ")
    if quad_x is False or quad_x < 1 or quad_x > 8:
        print "Invalid X coordinate."
        print
        return
    quad_y = input_double("Enter destination quadrant Y (1--8): ")
    if quad_y is False or quad_y < 1 or quad_y > 8:
        print "Invalid Y coordinate."
        print
        return
    print
    qx = int(quad_x) - 1
    qy = int(quad_y) - 1
    if qx == game.quadrant_x and qy == game.quadrant_y:
        print "That is the current location of the Enterprise."
        print
        return
    print "Direction: {0:1.2f}".format(compute_direction(
        game.quadrant_x, game.quadrant_y, qx, qy))
    print "Distance:  {0:2.2f}".format(
        distance(game.quadrant_x, game.quadrant_y, qx, qy))
    print


def starbase_calculator():
    global game
    print
    if game.quadrants[game.quadrant_y][game.quadrant_x].starbase:
        print "Starbase in sector [%s,%s]." % (
            game.starbase_x + 1, game.starbase_y + 1)
        print "Direction: {0:1.2f}".format(
            compute_direction(
                game.sector_x, game.sector_y, game.starbase_x, game.starbase_y)
        )
        print "Distance:  {0:2.2f}".format(distance(
            game.sector_x, game.sector_y, game.starbase_x, game.starbase_y) / 8)
    else:
        print "There are no starbases in this quadrant."
    print


def photon_torpedo_calculator():
    global game
    print
    if len(game.klingon_ships) == 0:
        print "There are no Klingon ships in this quadrant."
        print
        return

    for ship in game.klingon_ships:
        text = "Direction {2:1.2f}: Klingon ship in sector [{0},{1}]."
        print text.format(
            ship.sector_x + 1, ship.sector_y + 1,
            compute_direction(
                game.sector_x, game.sector_y, ship.sector_x, ship.sector_y))
    print


def display_status():
    global game
    print
    print "               Time Remaining: {0}".format(game.time_remaining)
    print "      Klingon Ships Remaining: {0}".format(game.klingons)
    print "                    Starbases: {0}".format(game.starbases)
    print "           Warp Engine Damage: {0}".format(game.navigation_damage)
    print "   Short Range Scanner Damage: {0}".format(
        game.short_range_scan_damage)
    print "    Long Range Scanner Damage: {0}".format(
        game.long_range_scan_damage)
    print "       Shield Controls Damage: {0}".format(
        game.shield_control_damage)
    print "         Main Computer Damage: {0}".format(game.computer_damage)
    print "Photon Torpedo Control Damage: {0}".format(game.photon_damage)
    print "                Phaser Damage: {0}".format(game.phaser_damage)
    print


def display_galactic_record():
    global game
    print
    sb = ""
    print "-------------------------------------------------"
    for i in range(8):
        for j in range(8):
            sb += "| "
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            quadrant = game.quadrants[i][j]
            if quadrant.scanned:
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
            sb = sb + \
                "{0}{1}{2} ".format(klingon_count, starbase_count, star_count)
        sb += "|"
        print sb
        sb = ""
        print "-------------------------------------------------"
    print


def phaser_controls():
    global game
    if game.phaser_damage > 0:
        print "Phasers are damaged. Repairs are underway."
        print
        return
    if len(game.klingon_ships) == 0:
        print "There are no Klingon ships in this quadrant."
        print
        return
    print "Phasers locked on target."
    phaser_energy = input_double("Enter phaser energy (1--{0}): ".format(
        game.energy))
    if not phaser_energy or phaser_energy < 1 or phaser_energy > game.energy:
        print "Invalid energy level."
        print
        return
    print
    print "Firing phasers..."
    destroyed_ships = []
    for ship in game.klingon_ships:
        game.energy -= int(phaser_energy)
        if game.energy < 0:
            game.energy = 0
            break
        dist = distance(
            game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
        delivered_energy = phaser_energy * (1.0 - dist / 11.3)
        ship.shield_level -= int(delivered_energy)
        if ship.shield_level <= 0:
            print "Klingon ship destroyed at sector [{0},{1}].".format(
                ship.sector_x + 1, ship.sector_y + 1)
            destroyed_ships.append(ship)
        else:
            print "Hit ship at sector [{0},{1}]." + \
                "Klingon shield strength dropped to {2}.".format(
                ship.sector_x + 1, ship.sector_y + 1, ship.shield_level)
    for ship in destroyed_ships:
        game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
        game.klingons -= 1
        game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
        game.klingon_ships.remove(ship)
    if len(game.klingon_ships) > 0:
        print
        klingons_attack()
    print


def shield_controls():
    global game
    print "--- Shield Controls ----------------"
    print "add = Add energy to shields."
    print "sub = Subtract energy from shields."
    print
    print "Enter shield control command: "
    command = raw_input("Enter shield control command: ").strip().lower()
    print
    if command == "add":
        adding = True
        max_transfer = game.energy
    elif command == "sub":
        adding = False
        max_transfer = game.shield_level
    else:
        print "Invalid command."
        print
        return
    transfer = input_double(
        "Enter amount of energy (1--{0}): ".format(max_transfer))
    if not transfer or transfer < 1 or transfer > max_transfer:
        print "Invalid amount of energy."
        print
        return
    print
    if adding:
        game.energy -= int(transfer)
        game.shield_level += int(transfer)
    else:
        game.energy += int(transfer)
        game.shield_level -= int(transfer)
    print "Shield strength is now {0}. Energy level is now {1}.".format(
        game.shield_level, game.energy)
    print


def klingons_attack():
    global game
    if len(game.klingon_ships) > 0:
        for ship in game.klingon_ships:
            if game.docked:
                print "Enterprise hit by ship at sector [{0},{1}]." + \
                    "No damage due to starbase shields.".format(
                    ship.sector_x + 1, ship.sector_y + 1)
            else:
                dist = distance(
                    game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
                delivered_energy = 300 * \
                    random.uniform(0.0, 1.0) * (1.0 - dist / 11.3)
                game.shield_level -= int(delivered_energy)
                if game.shield_level < 0:
                    game.shield_level = 0
                    game.destroyed = True
                print "Enterprise hit by ship at sector [{0},{1}]." + \
                    "Shields dropped to {2}.".format(
                    ship.sector_x + 1, ship.sector_y + 1, game.shield_level)
                if game.shield_level == 0:
                    return True
        return True
    return False


def distance(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    return sqrt(x * x + y * y)


def induce_damage(item):
    global game
    if random.randint(0, 6) > 0:
        return
    damage = 1 + random.randint(0, 4)
    if item < 0:
        item = random.randint(0, 6)
    if item == 0:
        game.navigation_damage = damage
        print "Warp engines are malfunctioning."
    elif item == 1:
        game.short_range_scan_damage = damage
        print "Short range scanner is malfunctioning."
    elif item == 2:
        game.long_range_scan_damage = damage
        print "Long range scanner is malfunctioning."
    elif item == 3:
        game.shield_control_damage = damage
        print "Shield controls are malfunctioning."
    elif item == 4:
        game.computer_damage = damage
        print "The main computer is malfunctioning."
    elif item == 5:
        game.photon_damage = damage
        print "Photon torpedo controls are malfunctioning."
    elif item == 6:
        game.phaser_damage = damage
        print "Phasers are malfunctioning."
    print


def repair_damage():
    global game
    if game.navigation_damage > 0:
        game.navigation_damage -= 1
        if game.navigation_damage == 0:
            print "Warp engines have been repaired."
        print
        return True
    if game.short_range_scan_damage > 0:
        game.short_range_scan_damage -= 1
        if game.short_range_scan_damage == 0:
            print "Short range scanner has been repaired."
        print
        return True
    if game.long_range_scan_damage > 0:
        game.long_range_scan_damage -= 1
        if game.long_range_scan_damage == 0:
            print "Long range scanner has been repaired."
        print
        return True
    if game.shield_control_damage > 0:
        game.shield_control_damage -= 1
        if game.shield_control_damage == 0:
            print "Shield controls have been repaired."
        print
        return True
    if game.computer_damage > 0:
        game.computer_damage -= 1
        if game.computer_damage == 0:
            print "The main computer has been repaired."
        print
        return True
    if game.photon_damage > 0:
        game.photon_damage -= 1
        if game.photon_damage == 0:
            print "Photon torpedo controls have been repaired."
        print
        return True
    if game.phaser_damage > 0:
        game.phaser_damage -= 1
        if game.phaser_damage == 0:
            print "Phasers have been repaired."
        print
        return True
    return False


def long_range_scan():
    global game
    if game.long_range_scan_damage > 0:
        print "Long range scanner is damaged. Repairs are underway."
        print
        return
    sb = ""
    print "-------------------"
    for i in range(game.quadrant_y - 1, game.quadrant_y+2):
        for j in range(game.quadrant_x - 1, game.quadrant_x+2):
            sb += "|"
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            if 0 <= i < 8 and 0 <= j < 8:
                quadrant = game.quadrants[i][j]
                quadrant.scanned = True
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
            if i == game.quadrant_y and j == game.quadrant_x:
                sb = sb + "<{0}{1}{2}>".format(
                    klingon_count, starbase_count, star_count)
            else:
                sb = sb + " {0}{1}{2} ".format(
                    klingon_count, starbase_count, star_count)

        sb += "|"
        print sb
        sb = ""
        print "-------------------"
    print


def torpedo_control():
    global game
    if game.photon_damage > 0:
        print "Photon torpedo control is damaged. Repairs are underway."
        print
        return
    if game.photon_torpedoes == 0:
        print "Photon torpedoes exhausted."
        print
        return
    if len(game.klingon_ships) == 0:
        print "There are no Klingon ships in this quadrant."
        print
        return
    direction = input_double("Enter firing direction (1.0--9.0): ")
    if not direction or direction < 1.0 or direction > 9.0:
        print "Invalid direction."
        print
        return
    print
    print "Photon torpedo fired..."
    game.photon_torpedoes -= 1
    angle = -(pi * (direction - 1.0) / 4.0)
    if random.randint(0, 2) == 0:
        angle += (1.0 - 2.0 * random.uniform(0.0, 1.0) * pi * 2.0) * 0.03
    x = game.sector_x
    y = game.sector_y
    vx = cos(angle) / 20
    vy = sin(angle) / 20
    last_x = last_y = -1
    # new_x = game.sector_x
    # new_y = game.sector_y
    hit = False
    while x >= 0 and y >= 0 and round(x) < 8 and round(y) < 8:
        new_x = int(round(x))
        new_y = int(round(y))
        if last_x != new_x or last_y != new_y:
            print "  [{0},{1}]".format(new_x + 1, new_y + 1)
            last_x = new_x
            last_y = new_y
        for ship in game.klingon_ships:
            if ship.sector_x == new_x and ship.sector_y == new_y:
                print "Klingon ship destroyed at sector [{0},{1}].".format(
                    ship.sector_x + 1, ship.sector_y + 1)
                game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
                game.klingons -= 1
                game.klingon_ships.remove(ship)
                game.quadrants[game.quadrant_y][game.quadrant_x].klingons -= 1
                hit = True
                break  # break out of the for loop
        if hit:
            break  # break out of the while loop
        if game.sector[new_y][new_x] == sector_type.starbase:
            game.starbases -= 1
            game.quadrants[game.quadrant_y][game.quadrant_x].starbase = False
            game.sector[new_y][new_x] = sector_type.empty
            print "The Enterprise destroyed a Federation starbase at sector [" \
                  "{0},{1}]!".format(new_x + 1, new_y + 1)
            hit = True
            break
        elif game.sector[new_y][new_x] == sector_type.star:
            print "The torpedo was captured by a star's gravitational field " \
                "at sector [{0},{1}].".format(new_x + 1, new_y + 1)
            hit = True
            break
        x += vx
        y += vy
    if not hit:
        print "Photon torpedo failed to hit anything."
    if len(game.klingon_ships) > 0:
        print
        klingons_attack()
    print


def navigation():
    global game
    max_warp_factor = 8.0
    if game.navigation_damage > 0:
        max_warp_factor = 0.2 + random.randint(0, 8) / 10.0
        print "Warp engines damaged. Maximum warp factor: {0}".format(
            max_warp_factor)
        print

    direction = input_double("Enter course (1.0--8.9): ")
    if not direction or direction < 1.0 or direction > 9.0:
        print "Invalid course."
        print
        return

    dist = input_double(
        "Enter warp factor (0.1--{0}): ".format(max_warp_factor))
    if not dist or dist < 0.1 or dist > max_warp_factor:
        print "Invalid warp factor."
        print
        return

    print

    dist *= 8
    energy_required = int(dist)
    if energy_required >= game.energy:
        print "Unable to comply. Insufficient energy to travel that speed."
        print
        return
    else:
        print "Warp engines engaged."
        print
        game.energy -= energy_required

    last_quad_x = game.quadrant_x
    last_quad_y = game.quadrant_y
    angle = -(pi * (direction - 1.0) / 4.0)
    x = game.quadrant_x * 8 + game.sector_x
    y = game.quadrant_y * 8 + game.sector_y
    dx = dist * cos(angle)
    dy = dist * sin(angle)
    vx = dx / 1000
    vy = dy / 1000
    # quad_x = quad_y = sect_x = sect_y = 0
    last_sect_x = game.sector_x
    last_sect_y = game.sector_y
    game.sector[game.sector_y][game.sector_x] = sector_type.empty
    obstacle = False
    for i in range(999):
        x += vx
        y += vy
        quad_x = int(round(x)) / 8
        quad_y = int(round(y)) / 8
        if quad_x == game.quadrant_x and quad_y == game.quadrant_y:
            sect_x = int(round(x)) % 8
            sect_y = int(round(y)) % 8
            if game.sector[sect_y][sect_x] != sector_type.empty:
                game.sector_x = last_sect_x
                game.sector_y = last_sect_y
                game.sector[game.sector_y][game.sector_x] = (
                    sector_type.enterprise)
                print "Encountered obstacle within quadrant."
                print
                obstacle = True
                break
            last_sect_x = sect_x
            last_sect_y = sect_y

    if not obstacle:
        if x < 0:
            x = 0
        elif x > 63:
            x = 63
        if y < 0:
            y = 0
        elif y > 63:
            y = 63
        quad_x = int(round(x)) / 8
        quad_y = int(round(y)) / 8
        game.sector_x = int(round(x)) % 8
        game.sector_y = int(round(y)) % 8
        if quad_x != game.quadrant_x or quad_y != game.quadrant_y:
            game.quadrant_x = quad_x
            game.quadrant_y = quad_y
            generate_sector()
        else:
            game.quadrant_x = quad_x
            game.quadrant_y = quad_y
            game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
    if is_docking_location(game.sector_y, game.sector_x):
        game.energy = 3000
        game.photon_torpedoes = 10
        game.navigation_damage = 0
        game.short_range_scan_damage = 0
        game.long_range_scan_damage = 0
        game.shield_control_damage = 0
        game.computer_damage = 0
        game.photon_damage = 0
        game.phaser_damage = 0
        game.shield_level = 0
        game.docked = True
    else:
        game.docked = False

    if last_quad_x != game.quadrant_x or last_quad_y != game.quadrant_y:
        game.time_remaining -= 1
        game.star_date += 1

    short_range_scan()

    if game.docked:
        print "Lowering shields as part of docking sequence..."
        print "Enterprise successfully docked with starbase."
        print
    else:
        if game.quadrants[game.quadrant_y][game.quadrant_x].klingons > 0 and \
                last_quad_x == game.quadrant_x and \
                last_quad_y == game.quadrant_y:
            klingons_attack()
            print
        elif not repair_damage():
            induce_damage(-1)


def input_double(prompt):
    text = raw_input(prompt)
    if text == "":
        return False
    value = float(text)
    if type(value) == float:
        return value
    else:
        return False


def generate_sector():
    global game
    quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
    starbase = quadrant.starbase
    stars = quadrant.stars
    klingons = quadrant.klingons
    game.klingon_ships = []
    for i in range(8):
        for j in range(8):
            game.sector[i][j] = sector_type.empty
    game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
    while starbase or stars > 0 or klingons > 0:
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        if is_sector_region_empty(i, j):
            if starbase:
                starbase = False
                game.sector[i][j] = sector_type.starbase
                game.starbase_y = i
                game.starbase_x = j
            elif stars > 0:
                game.sector[i][j] = sector_type.star
                stars -= 1
            elif klingons > 0:
                game.sector[i][j] = sector_type.klingon
                klingon_ship = KlingonShip()
                klingon_ship.shield_level = 300 + random.randint(0, 199)
                klingon_ship.sector_y = i
                klingon_ship.sector_x = j
                game.klingon_ships.append(klingon_ship)
                klingons -= 1


def is_docking_location(i, j):
    for y in range(i - 1, i+1):  # i + 1?
        for x in range(j - 1, j+1):  # j + 1?
            if read_sector(y, x) == sector_type.starbase:
                return True
    return False


def is_sector_region_empty(i, j):
    for y in range(i - 1, i+1):  # i + 1?
        if read_sector(y, j - 1) != sector_type.empty and \
                read_sector(y, j + 1) != sector_type.empty:
            return False
    return read_sector(i, j) == sector_type.empty


def read_sector(i, j):
    global game
    if i < 0 or j < 0 or i > 7 or j > 7:
        return sector_type.empty
    return game.sector[i][j]


def short_range_scan():
    global game
    if game.short_range_scan_damage > 0:
        print "Short range scanner is damaged. Repairs are underway."
        print
    else:
        quadrant = game.quadrants[game.quadrant_y][game.quadrant_x]
        quadrant.scanned = True
        print_sector(quadrant)
    print


def print_sector(quadrant):
    global game
    game.condition = "GREEN"
    if quadrant.klingons > 0:
        game.condition = "RED"
    elif game.energy < 300:
        game.condition = "YELLOW"

    sb = ""
    print "-=--=--=--=--=--=--=--=-          Region: {0}".format(quadrant.name)
    print_sector_row(sb, 0, "           Quadrant: [{0},{1}]".format(
        game.quadrant_x + 1, game.quadrant_y + 1))
    print_sector_row(sb, 1, "             Sector: [{0},{1}]".format(
        game.sector_x + 1, game.sector_y + 1))
    print_sector_row(sb, 2, "           Stardate: {0}".format(game.star_date))
    print_sector_row(sb, 3, "     Time remaining: {0}".format(
        game.time_remaining))
    print_sector_row(sb, 4, "          Condition: {0}".format(game.condition))
    print_sector_row(sb, 5, "             Energy: {0}".format(game.energy))
    print_sector_row(sb, 6, "            Shields: {0}".format(
        game.shield_level))
    print_sector_row(sb, 7, "   Photon Torpedoes: {0}".format(
        game.photon_torpedoes))
    print "-=--=--=--=--=--=--=--=-             Docked: {0}".format(game.docked)

    if quadrant.klingons > 0:
        print
        print "Condition RED: Klingon ship{0} detected.".format(
            "" if quadrant.klingons == 1 else "s")
        if game.shield_level == 0 and not game.docked:
            print "Warning: Shields are down."
    elif game.energy < 300:
        print
        print "Condition YELLOW: Low energy level."
        game.condition = "YELLOW"


def print_sector_row(sb, row, suffix):
    global game
    for column in range(8):
        if game.sector[row][column] == sector_type.empty:
            sb += "   "
        elif game.sector[row][column] == sector_type.enterprise:
            sb += "<E>"
        elif game.sector[row][column] == sector_type.klingon:
            sb += "+K+"
        elif game.sector[row][column] == sector_type.star:
            sb += " * "
        elif game.sector[row][column] == sector_type.starbase:
            sb += ">S<"
    if suffix is not None:
        sb = sb + suffix
    print sb


def print_mission():
    global game
    print "Mission: Destroy {0} Klingon ships in {1} stardates " \
        "with {2} starbases.".format(
        game.klingons, game.time_remaining, game.starbases)
    print


def initialize_game():
    # gah, globals
    global game
    game.quadrant_x = random.randint(0, 7)
    game.quadrant_y = random.randint(0, 7)
    game.sector_x = random.randint(0, 7)
    game.sector_y = random.randint(0, 7)
    game.star_date = random.randint(0, 50) + 2250
    game.energy = 3000
    game.photon_torpedoes = 10
    game.time_remaining = 40 + random.randint(0, 9)
    game.klingons = 15 + random.randint(0, 5)
    game.starbases = 2 + random.randint(0, 2)
    game.destroyed = False
    game.navigation_damage = 0
    game.short_range_scan_damage = 0
    game.long_range_scan_damage = 0
    game.shield_control_damage = 0
    game.computer_damage = 0
    game.photon_damage = 0
    game.phaser_damage = 0
    game.shield_level = 0
    game.docked = False

    names = []
    for name in strings.quadrant_names:
        names.append(name)

    for i in range(8):
        for j in range(8):
            index = random.randint(0, len(names) - 1)
            quadrant = Quadrant()
            quadrant.name = names[index]
            quadrant.stars = 1 + random.randint(0, 7)
            game.quadrants[i][j] = quadrant
            del names[index]

    klingon_count = game.klingons
    starbase_count = game.starbases
    while klingon_count > 0 or starbase_count > 0:
        i = random.randint(0, 7)
        j = random.randint(0, 7)
        quadrant = game.quadrants[i][j]
        if not quadrant.starbase:
            quadrant.starbase = True
            starbase_count -= 1
        if quadrant.klingons < 3:
            quadrant.klingons += 1
            klingon_count -= 1


def print_strings(string_list):
    for string in string_list:
        print string
    print


if __name__ == '__main__':
    run()

"""
Star Trek 1971
Forked from https://github.com/cosmicr/startrek1971
Not sure why yet.
"""


from math import atan2, pi, sqrt, cos, sin
import random
import sys

import strings


class Quadrant:
    """Quadrant Object"""

    def __init__(self):
        self.name = ""
        self.klingons = 0
        self.stars = 0
        self.starbase = False
        self.scanned = False


class SectorType:
    """I guess an object to define sector types"""

    def __init__(self):
        self.empty, self.star, self.klingon, self.enterprise, self.starbase = (
            1,
            2,
            3,
            4,
            5,
        )


sector_type = SectorType()


class KlingonShip:
    """Klingon ship object."""

    def __init__(self):
        self.sector_x = 0
        self.sector_y = 0
        self.shield_level = 0


class Game:
    """Game Object, so it must be important."""

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
        self.condition = ""


game = Game()


def run():
    """Looks like the main loop."""
    print_strings(strings.titleStrings)
    while True:
        initialize_game()
        print_mission()
        generate_sector()
        print_strings(strings.commandStrings)
        while (
            game.energy > 0
            and not game.destroyed
            and game.klingons > 0
            and game.time_remaining > 0
        ):
            command_prompt()
            print_game_status()


def print_game_status():
    """Displays final game outcome."""
    if game.destroyed:
        print("MISSION FAILED: ENTERPRISE DESTROYED!!!\r\n\n\n")
    elif game.energy == 0:
        print("MISSION FAILED: ENTERPRISE RAN OUT OF ENERGY.\r\n\n\n")
    elif game.klingons == 0:
        print("MISSION ACCOMPLISHED: ALL KLINGON SHIPS DESTROYED. WELL DONE!!!\r\n\n\n")
    elif game.time_remaining == 0:
        print("MISSION FAILED: ENTERPRISE RAN OUT OF TIME.\r\n\n\n")


def command_prompt():
    """Prompt user for command, then go do it."""
    command = input("Enter command: ").strip().lower()
    print()
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
    elif command.startswith("qui") or command.startswith("exi"):
        sys.exit()
    else:
        print_strings(strings.commandStrings)


def computer_controls():
    """Prompt user for computer commands, then jump to them."""
    if game.computer_damage > 0:
        print("The main computer is damaged. Repairs are underway.\r\n")
        return
    print_strings(strings.computerStrings)
    command = input("Enter computer command: ").strip().lower()
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
        print("\r\nInvalid computer command.\r\n")
    induce_damage(4)


def compute_direction(col_1, row_1, col_2, row_2):
    """Returns a direction of some sort."""
    if col_1 == col_2:
        if row_1 < row_2:
            direction = 7
        else:
            direction = 3
    elif row_1 == row_2:
        if col_1 < col_2:
            direction = 1
        else:
            direction = 5
    else:
        delta_row = abs(row_2 - row_1)
        delta_col = abs(col_2 - col_1)
        radian_angle = atan2(delta_row, delta_col)
        if col_1 < col_2:
            if row_1 < row_2:
                direction = 9.0 - 4.0 * radian_angle / pi
            else:
                direction = 1.0 + 4.0 * radian_angle / pi
        else:
            if row_1 < row_2:
                direction = 5.0 + 4.0 * radian_angle / pi
            else:
                direction = 5.0 - 4.0 * radian_angle / pi
    return direction


def navigation_calculator():
    """Calulates Direction and Distance."""
    print(
        f"\r\nEnterprise located in quadrant [{game.quadrant_x + 1},{game.quadrant_y + 1}].\r\n"
    )
    quad_x = input_double("Enter destination quadrant X (1--8): ")
    if quad_x is False or quad_x < 1 or quad_x > 8:
        print("Invalid X coordinate.\r\n")
        return
    quad_y = input_double("Enter destination quadrant Y (1--8): ")
    if quad_y is False or quad_y < 1 or quad_y > 8:
        print("Invalid Y coordinate.\r\n")
        return
    print()
    q_x = int(quad_x) - 1
    q_y = int(quad_y) - 1
    if q_x == game.quadrant_x and q_y == game.quadrant_y:
        print("That is the current location of the Enterprise.\r\n")
        return
    print(
        "Direction: {0:1.2f}".format(
            compute_direction(game.quadrant_x, game.quadrant_y, q_x, q_y)
        )
    )
    print(
        "Distance:  {0:2.2f}".format(
            distance(game.quadrant_x, game.quadrant_y, q_x, q_y)
        )
    )
    print()


def starbase_calculator():
    """Shows if and where a Starbase is in a quadrant."""
    print()
    if game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)].starbase:
        print(f"Starbase in sector [{game.starbase_x + 1},{game.starbase_y + 1}].")
        print(
            "Direction: {0:1.2f}".format(
                compute_direction(
                    game.sector_x, game.sector_y, game.starbase_x, game.starbase_y
                )
            )
        )
        print(
            "Distance:  {0:2.2f}".format(
                distance(game.sector_x, game.sector_y, game.starbase_x, game.starbase_y)
                / 8
            )
        )
    else:
        print("There are no starbases in this quadrant.")
    print()


def photon_torpedo_calculator():
    """Prints if and where Klingon ships in the sector are."""
    print()
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.\r\n")
        return

    for ship in game.klingon_ships:
        text = "Direction {2:1.2f}: Klingon ship in sector [{0},{1}].".format(
            ship.sector_x + 1,
            ship.sector_y + 1,
            compute_direction(
                game.sector_x, game.sector_y, ship.sector_x, ship.sector_y
            ),
        )
        print(text)
    print()


def display_status():
    """Displays the status"""
    print(f"\r\n               Time Remaining: {game.time_remaining}")
    print(f"      Klingon Ships Remaining: {game.klingons}")
    print(f"                    Starbases: {game.starbases}")
    print(f"           Warp Engine Damage: {game.navigation_damage}")
    print(f"   Short Range Scanner Damage: {game.short_range_scan_damage}")
    print(f"    Long Range Scanner Damage: {game.long_range_scan_damage}")
    print(f"       Shield Controls Damage: {game.shield_control_damage}")
    print(f"         Main Computer Damage: {game.computer_damage}")
    print(f"Photon Torpedo Control Damage: {game.photon_damage}")
    print(f"                Phaser Damage: {game.phaser_damage}\r\n")


def display_galactic_record():
    """I think it shows known objects"""
    scanned_block = ""
    print("\r\n-------------------------------------------------")
    for i in range(8):
        for j in range(8):
            scanned_block += "| "
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            quadrant = game.quadrants[i][j]
            if quadrant.scanned:
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
            scanned_block = (
                scanned_block + f"{klingon_count}{starbase_count}{star_count} "
            )
        scanned_block += "|"
        print(scanned_block)
        scanned_block = ""
        print("-------------------------------------------------")
    print()


def phaser_controls():
    """Process a phaser interaction."""
    if game.phaser_damage > 0:
        print("Phasers are damaged. Repairs are underway.\r\n")
        return
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.\r\n")
        return
    print("Phasers locked on target.")
    phaser_energy = input_double(f"Enter phaser energy (1--{game.energy}): ")
    if not phaser_energy or phaser_energy < 1 or phaser_energy > game.energy:
        print("Invalid energy level.\r\n")
        return
    print()
    print("Firing phasers...")
    destroyed_ships = []
    for ship in game.klingon_ships:
        game.energy -= int(phaser_energy)
        if game.energy < 0:
            game.energy = 0
            break
        dist = distance(game.sector_x, game.sector_y, ship.sector_x, ship.sector_y)
        delivered_energy = phaser_energy * (1.0 - dist / 11.3)
        ship.shield_level -= int(delivered_energy)
        if ship.shield_level <= 0:
            print(
                f"Klingon ship destroyed at sector [{ship.sector_x + 1},{ship.sector_y + 1}]."
            )
            destroyed_ships.append(ship)
        else:
            print(
                f"Hit ship at sector [{ship.sector_x + 1},{ship.sector_y + 1}]. "
                f"Klingon shield strength dropped to {ship.shield_level}."
            )
    for ship in destroyed_ships:
        game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)].klingons -= 1
        game.klingons -= 1
        game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
        game.klingon_ships.remove(ship)
    if len(game.klingon_ships) > 0:
        print()
        klingons_attack()
    print()


def shield_controls():
    """Manipulate your shields."""
    print("--- Shield Controls ----------------")
    print("add = Add energy to shields.")
    print("sub = Subtract energy from shields.\r\n")
    print("Enter shield control command: ")
    command = input("Enter shield control command: ").strip().lower()
    print()
    if command == "add":
        adding = True
        max_transfer = game.energy
    elif command == "sub":
        adding = False
        max_transfer = game.shield_level
    else:
        print("Invalid command.\r\n")
        return
    transfer = input_double(f"Enter amount of energy (1--{max_transfer}): ")
    if not transfer or transfer < 1 or transfer > max_transfer:
        print("Invalid amount of energy.\r\n")
        return
    print()
    if adding:
        game.energy -= int(transfer)
        game.shield_level += int(transfer)
    else:
        game.energy += int(transfer)
        game.shield_level -= int(transfer)
    print(
        f"Shield strength is now {game.shield_level}. Energy level is now {game.energy}.\r\n"
    )


def klingons_attack():
    """Klingons... Better than Vogons."""
    if len(game.klingon_ships) > 0:
        for ship in game.klingon_ships:
            if game.docked:
                print(
                    f"Enterprise hit by ship at sector [{ship.sector_x + 1},{ship.sector_y + 1}]. "
                    "No damage due to starbase shields."
                )
            else:
                dist = distance(
                    game.sector_x, game.sector_y, ship.sector_x, ship.sector_y
                )
                delivered_energy = 300 * random.uniform(0.0, 1.0) * (1.0 - dist / 11.3)
                game.shield_level -= int(delivered_energy)
                if game.shield_level < 0:
                    game.shield_level = 0
                    game.destroyed = True
                print(
                    f"Enterprise hit by ship at sector [{ship.sector_x + 1},{ship.sector_y + 1}]. "
                    f"Shields dropped to {game.shield_level}."
                )
                if game.shield_level == 0:
                    return True
        return True
    return False


def distance(col_1, row_1, col_2, row_2):
    """Computes distance of two objects."""
    column = col_2 - col_1
    row = row_2 - row_1
    return sqrt(column * column + row * row)


def induce_damage(item):
    """I gotta owie."""
    if random.randint(0, 6) > 0:
        return
    damage = 1 + random.randint(0, 4)
    if item < 0:
        item = random.randint(0, 6)
    if item == 0:
        game.navigation_damage = damage
        print("Warp engines are malfunctioning.")
    elif item == 1:
        game.short_range_scan_damage = damage
        print("Short range scanner is malfunctioning.")
    elif item == 2:
        game.long_range_scan_damage = damage
        print("Long range scanner is malfunctioning.")
    elif item == 3:
        game.shield_control_damage = damage
        print("Shield controls are malfunctioning.")
    elif item == 4:
        game.computer_damage = damage
        print("The main computer is malfunctioning.")
    elif item == 5:
        game.photon_damage = damage
        print("Photon torpedo controls are malfunctioning.")
    elif item == 6:
        game.phaser_damage = damage
        print("Phasers are malfunctioning.")
    print()


def repair_damage():
    """Kiss it and make it better."""
    if game.navigation_damage > 0:
        game.navigation_damage -= 1
        if game.navigation_damage == 0:
            print("Warp engines have been repaired.")
        print()
        return True
    if game.short_range_scan_damage > 0:
        game.short_range_scan_damage -= 1
        if game.short_range_scan_damage == 0:
            print("Short range scanner has been repaired.")
        print()
        return True
    if game.long_range_scan_damage > 0:
        game.long_range_scan_damage -= 1
        if game.long_range_scan_damage == 0:
            print("Long range scanner has been repaired.")
        print()
        return True
    if game.shield_control_damage > 0:
        game.shield_control_damage -= 1
        if game.shield_control_damage == 0:
            print("Shield controls have been repaired.")
        print()
        return True
    if game.computer_damage > 0:
        game.computer_damage -= 1
        if game.computer_damage == 0:
            print("The main computer has been repaired.")
        print()
        return True
    if game.photon_damage > 0:
        game.photon_damage -= 1
        if game.photon_damage == 0:
            print("Photon torpedo controls have been repaired.")
        print()
        return True
    if game.phaser_damage > 0:
        game.phaser_damage -= 1
        if game.phaser_damage == 0:
            print("Phasers have been repaired.")
        print()
        return True
    return False


def long_range_scan():
    """Perform Long range scan."""
    if game.long_range_scan_damage > 0:
        print("Long range scanner is damaged. Repairs are underway.\r\n")
        return
    scanned_block = ""
    print("-------------------")
    for i in range(
        int(game.quadrant_y) - 1, int(game.quadrant_y) + 2
    ):  # quadrantY + 1 ?
        for j in range(
            int(game.quadrant_x) - 1, int(game.quadrant_x) + 2
        ):  # quadrantX + 1?
            scanned_block += "| "
            klingon_count = 0
            starbase_count = 0
            star_count = 0
            if 0 <= i < 8 and 0 <= j < 8:
                quadrant = game.quadrants[i][j]
                quadrant.scanned = True
                klingon_count = quadrant.klingons
                starbase_count = 1 if quadrant.starbase else 0
                star_count = quadrant.stars
            scanned_block = (
                scanned_block + f"{klingon_count}{starbase_count}{star_count} "
            )
        scanned_block += "|"
        print(scanned_block)
        scanned_block = ""
        print("-------------------")
    print()


def torpedo_control():
    """Process torpedo interaction."""
    if game.photon_damage > 0:
        print("Photon torpedo control is damaged. Repairs are underway.\r\n")
        return
    if game.photon_torpedoes == 0:
        print("Photon torpedoes exhausted.\r\n")
        return
    if len(game.klingon_ships) == 0:
        print("There are no Klingon ships in this quadrant.\r\n")
        return
    direction = input_double("Enter firing direction (1.0--9.0): ")
    if not direction or direction < 1.0 or direction > 9.0:
        print("Invalid direction.\r\n")
        return
    print("\r\nPhoton torpedo fired...")
    game.photon_torpedoes -= 1
    angle = -(pi * (direction - 1.0) / 4.0)
    if random.randint(0, 2) == 0:
        angle += (1.0 - 2.0 * random.uniform(0.0, 1.0) * pi * 2.0) * 0.03
    col = game.sector_x
    row = game.sector_y
    v_x = cos(angle) / 20
    v_y = sin(angle) / 20
    last_x = last_y = -1
    # new_x = game.sector_x
    # new_y = game.sector_y
    hit = False
    while col >= 0 and row >= 0 and round(col) < 8 and round(row) < 8:
        new_x = int(round(col))
        new_y = int(round(row))
        if last_x != new_x or last_y != new_y:
            print(f"  [{new_x + 1},{new_y + 1}]")
            last_x = new_x
            last_y = new_y
        for ship in game.klingon_ships:
            if ship.sector_x == new_x and ship.sector_y == new_y:
                print(
                    f"Klingon ship destroyed at sector [{ship.sector_x + 1},{ship.sector_y + 1}]."
                )
                game.sector[ship.sector_y][ship.sector_x] = sector_type.empty
                game.klingons -= 1
                game.klingon_ships.remove(ship)
                game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)].klingons -= 1
                hit = True
                break  # break out of the for loop
        if hit:
            break  # break out of the while loop
        if game.sector[new_y][new_x] == sector_type.starbase:
            game.starbases -= 1
            game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)].starbase = False
            game.sector[new_y][new_x] = sector_type.empty
            print(
                "The Enterprise destroyed a Federation starbase at sector "
                f"[{new_x + 1},{new_y + 1}]!"
            )
            hit = True
            break
        if game.sector[new_y][new_x] == sector_type.star:
            print(
                "The torpedo was captured by a star's gravitational field at sector "
                f"[{new_x + 1},{new_y + 1}]."
            )
            hit = True
            break
        col += v_x
        row += v_y
    if not hit:
        print("Photon torpedo failed to hit anything.")
    if len(game.klingon_ships) > 0:
        print()
        klingons_attack()
    print()


def navigation():
    """Move Bitch, Get out the way."""
    max_warp_factor = 8.0
    if game.navigation_damage > 0:
        max_warp_factor = 0.2 + random.randint(0, 8) / 10.0
        print(f"Warp engines damaged. Maximum warp factor: {max_warp_factor}\r\n")

    direction = input_double("Enter course (1.0--8.9): ")
    if not direction or direction < 1.0 or direction > 9.0:
        print_strings(strings.compass_rose)
        # print("Invalid course.\r\n")
        return

    dist = input_double(f"Enter warp factor (0.1--{max_warp_factor}): ")
    if not dist or dist < 0.1 or dist > max_warp_factor:
        print("Invalid warp factor.\r\n")
        return

    print()

    dist *= 8
    energy_required = int(dist)
    if energy_required >= game.energy:
        print("Unable to comply. Insufficient energy to travel that speed.\r\n")
        return
    else:
        print("Warp engines engaged.\r\n")
        game.energy -= energy_required

    last_quad_x = game.quadrant_x
    last_quad_y = game.quadrant_y
    angle = -(pi * (direction - 1.0) / 4.0)
    col = game.quadrant_x * 8 + game.sector_x
    row = game.quadrant_y * 8 + game.sector_y
    d_x = dist * cos(angle)
    d_y = dist * sin(angle)
    v_x = d_x / 1000
    v_y = d_y / 1000
    # quad_x = quad_y = sect_x = sect_y = 0
    last_sect_x = game.sector_x
    last_sect_y = game.sector_y
    game.sector[game.sector_y][game.sector_x] = sector_type.empty
    obstacle = False
    for _ in range(999):
        col += v_x
        row += v_y
        quad_x = int(round(col)) / 8
        quad_y = int(round(row)) / 8
        if quad_x == game.quadrant_x and quad_y == game.quadrant_y:
            sect_x = int(round(col)) % 8
            sect_y = int(round(row)) % 8
            if game.sector[sect_y][sect_x] != sector_type.empty:
                game.sector_x = last_sect_x
                game.sector_y = last_sect_y
                game.sector[game.sector_y][game.sector_x] = sector_type.enterprise
                print("Encountered obstacle within quadrant.\r\n")
                obstacle = True
                break
            last_sect_x = sect_x
            last_sect_y = sect_y

    if not obstacle:
        if col < 0:
            col = 0
        elif col > 63:
            col = 63
        if row < 0:
            row = 0
        elif row > 63:
            row = 63
        quad_x = int(round(col)) / 8
        quad_y = int(round(row)) / 8
        game.sector_x = int(round(col)) % 8
        game.sector_y = int(round(row)) % 8
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
        print("Lowering shields as part of docking sequence...")
        print("Enterprise successfully docked with starbase.\r\n")
    else:
        if (
            game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)].klingons > 0
            and last_quad_x == game.quadrant_x
            and last_quad_y == game.quadrant_y
        ):
            klingons_attack()
            print()
        elif not repair_damage():
            induce_damage(-1)


def input_double(prompt):
    """Get floatingpoint number"""
    text = input(prompt)
    try:
        value = float(text)
    except ValueError:
        return False
    if isinstance(value, float):
        return value
    else:
        return False


def generate_sector():
    """Make a sector"""
    quadrant = game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)]
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
    """I'm assuming it's checking to see if we can dock."""
    for row in range(i - 1, i + 1):  # i + 1?
        for col in range(j - 1, j + 1):  # j + 1?
            if read_sector(row, col) == sector_type.starbase:
                return True
    return False


def is_sector_region_empty(i, j):
    """Checks if sa sector is empty."""
    for row in range(i - 1, i + 1):  # i + 1?
        if (
            read_sector(row, j - 1) != sector_type.empty
            and read_sector(row, j + 1) != sector_type.empty
        ):
            return False
    return read_sector(i, j) == sector_type.empty


def read_sector(i, j):
    """Gets contents of sector."""
    if i < 0 or j < 0 or i > 7 or j > 7:
        return sector_type.empty
    return game.sector[i][j]


def short_range_scan():
    """Do a srs."""
    if game.short_range_scan_damage > 0:
        print("Short range scanner is damaged. Repairs are underway.\r\n")
    else:
        quadrant = game.quadrants[int(game.quadrant_y)][int(game.quadrant_x)]
        quadrant.scanned = True
        print_sector(quadrant)
    print()


def print_sector(quadrant):
    """Display whats in a sector."""
    game.condition = "GREEN"
    if quadrant.klingons > 0:
        game.condition = "RED"
    elif game.energy < 300:
        game.condition = "YELLOW"

    scanned_block = ""
    print(f"-=--=--=--=--=--=--=--=-             Region: {quadrant.name}")
    print_sector_row(
        scanned_block,
        0,
        f"           Quadrant: [{int(game.quadrant_x + 1)},{int(game.quadrant_y + 1)}]",
    )
    print_sector_row(
        scanned_block,
        1,
        f"             Sector: [{game.sector_x + 1},{game.sector_y + 1}]",
    )
    print_sector_row(
        scanned_block, 2, "           Stardate: {0}".format(game.star_date)
    )
    print_sector_row(
        scanned_block, 3, "     Time remaining: {0}".format(game.time_remaining)
    )
    print_sector_row(
        scanned_block, 4, "          Condition: {0}".format(game.condition)
    )
    print_sector_row(scanned_block, 5, "             Energy: {0}".format(game.energy))
    print_sector_row(
        scanned_block, 6, "            Shields: {0}".format(game.shield_level)
    )
    print_sector_row(
        scanned_block, 7, "   Photon Torpedoes: {0}".format(game.photon_torpedoes)
    )
    print(f"-=--=--=--=--=--=--=--=-             Docked: {game.docked}")

    if quadrant.klingons > 0:
        print(
            f"\r\nCondition RED: Klingon ship{'' if quadrant.klingons == 1 else 's'} detected."
        )
        if game.shield_level == 0 and not game.docked:
            print("Warning: Shields are down.")
    elif game.energy < 300:
        print("\r\nCondition YELLOW: Low energy level.")
        game.condition = "YELLOW"


def print_sector_row(scanned_block, row, suffix):
    """Print out whats in a sectors row."""
    for column in range(8):
        if game.sector[row][column] == sector_type.empty:
            scanned_block += "   "
        elif game.sector[row][column] == sector_type.enterprise:
            scanned_block += "<E>"
        elif game.sector[row][column] == sector_type.klingon:
            scanned_block += "+K+"
        elif game.sector[row][column] == sector_type.star:
            scanned_block += " * "
        elif game.sector[row][column] == sector_type.starbase:
            scanned_block += ">S<"
    if suffix is not None:
        scanned_block = scanned_block + suffix
    print(scanned_block)


def print_mission():
    """Yup show the mission."""
    print(
        f"Mission: Destroy {game.klingons} "
        f"Klingon ships in {game.time_remaining} "
        f"stardates with {game.starbases} starbases.\r\n"
    )


def initialize_game():
    """Initalize game objects.."""
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
    for name in strings.quadrantNames:
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
    """Print list object."""
    for string in string_list:
        print(string)
    print()


if __name__ == "__main__":
    run()

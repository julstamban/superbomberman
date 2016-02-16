import random, math

# Each tuple is: (graphics, structure, palettes, graphic list, forced features, optional features)
# Not included yet: areas from battle mode
areas = [
    ("peace_town_graphic", "peace_town_level_structure", "peace_town_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR peace_town_unshaded_soft_animation
        .WORD 6
        .FARADDR tile_animation
        .FARADDR peace_town_shaded_soft_animation
        .WORD 2""", ".FARADDR create_random_bomb_drop"),
    ("village_graphic", "village_level_structure", "village_palettes", "standard_level_graphics", "", ""),
    ("castle_graphic", "castle_level_structure", "castle_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C51E3C
        .WORD 6
        .FARADDR tile_animation
        .FARADDR byte_C51E3C
        .WORD 2""", ""),
    ("park_graphic", "park_level_structure", "park_palettes", "standard_level_graphics", "", ""),
    ("circus_graphic", "circus_level_structure", "circus_palettes", "standard_level_graphics", "", """
        .FARADDR tile_animation
        .FARADDR byte_C522FA
        .WORD 6
        .FARADDR tile_animation
        .FARADDR byte_C523FF
        .WORD 2"""),
    ("garden_graphic", "garden_level_structure", "garden_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C52565
        .WORD 6
        .FARADDR tile_animation
        .FARADDR byte_C52688
        .WORD 2""", ".FARADDR create_flower_zone_handler"),
    ("factory_graphic", "factory_level_structure", "factory_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C52504
        .WORD 2
        .FARADDR tile_animation
        .FARADDR byte_C52504
        .WORD 6
        .FARADDR create_moving_platforms""", ""),
    ("dome_graphic", "dome_level_structure", "dome_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C51FED
        .WORD 6
        .FARADDR tile_animation
        .FARADDR byte_C5200C
        .WORD 2""", ""),
    ("speed_zone_graphic", "speed_zone_level_structure", "speed_zone_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C52854
        .WORD 2
        .FARADDR tile_animation
        .FARADDR byte_C52854
        .WORD 6""", ""),
    ("diamond_tower_tileset_graphic", "diamond_tower_level_structure", "diamond_tower_palettes", "standard_level_graphics", """
        .FARADDR tile_animation
        .FARADDR byte_C527F3
        .WORD 4""", ""),

    # Stages from battle mode
    ("normal_zone_graphic", "normal_zone_level_structure", "normal_zone_level_palettes", "standard_level_graphics", "", ""),
    ("tunnel_zone_graphic", "tunnel_zone_level_structure", "tunnel_zone_level_palettes", "standard_level_graphics", "", ""),
    ("warp_zone_graphic", "warp_zone_level_structure", "warp_zone_level_palettes", "standard_level_graphics", "", ""),
]

easy_enemies = [(1, x) for x in ["banen", "douken", "kouraru", "starnuts", "propene"]]
medium_enemies = [(1.4, x) for x in ["anzenda", "denkyun", "kierun" ]] + [(2, x) for x in ["bakuda", "chameleoman", "cuppen", "dengurin",  "kuwagen"]]
hard_enemies = [(3, x) for x in ["keibin", "kinkaru", "metal_kuwagen", "metal_propene", "metal_u", "moguchan", "pakupa", "red_bakuda", "robocom", "senshiyan"]] + [(5, "yoroisu")]

random.shuffle(easy_enemies)
random.shuffle(medium_enemies)
random.shuffle(hard_enemies)

basic_bonuses = ["BOMB_UP", "BOMB_UP", "BOMB_UP", "FIRE_UP", "FIRE_UP", "SPEED_UP"]
special_bonuses = ["REMOTE_CONTROL", "BOMB_PASS", "WALL_PASS", "RED_BOMBS", "KICK", "PUNCH", "FULL_FIRE"]
random.shuffle(special_bonuses)
diff_reduce_bonuses = ["VEST", "EXTRA_LIFE", "EXTRA_TIME"]
hidden_bonuses = ["RANDOM", "RANDOM", "RANDOM", "ONIGIRI", "CAKE", "KENDAMA", "APPLE", "FIRE_EXT", "POPSICLE", "ICE_CREAM"]

def difficulty_for_level(world, level):
    return math.sqrt(world * 5 + level + 3) * 5 - 12

def generate_random_level(world, level):
    area = areas[world_areas[world - 1][level - 1]]
    print """
    .BYTE $E
    .BYTE 0
    .BYTE 1         ; Spawn spot index and flags
                    ; Bit   1: Power Mode (Battle mode only)
                    ; Bit   2: Western mode, but without not-allowed soft-block locations (Battle mode only)
                    ; Bit   4: Required for Light Zone to correctly display the scoreboard
                    ; Bit   8: Disable soft blocks inside tunnels in tunnel zone
                    ; Bit $10: Belt Mode
                    ; Bit $20: Unused?
                    ; Bit $40: Used in Flower Zone, NOT related to flower growth, tractors or clouds.
                    ; Bit $80: Default tile and pallete IDs for hard block and empty tiles
    .BYTE 0         ; More flags
    .WORD 2         ; Screen mode. Always 2 for story mode stages
    .WORD $50       ; saved_to_d3a, unknown
    .FARADDR %s ; Tileset graphic
    .FARADDR bomb_and_explosions_graphic ; Bomb overlay graphic
    .FARADDR empty_tilemap ; Foreground Tileset (Despite the default being a tilemap!)
    .FARADDR %s ; Level structure
    .FARADDR empty_tilemap ; Foreground Tilemap
    .WORD $%x        ; level_representation
    .WORD %d         ; hard_blocks
    .WORD %d         ; soft_blocks
                     ; Off by one in    story mode, for    the level exit
    .FARADDR load_palettes; Init functions and their parameters
    .FARADDR %s
    .WORD $10 ; Number of palettes
    .BYTE 0 ; Unused?
    .FARADDR load_global_sprites
    .FARADDR %s
    .WORD $10 ; Number of graphic lists
    .BYTE 0 ; Unused?""" % (area[0], area[1], world * 16 + level, random.randint(0, 28), random.randint(20, 36), area[2], area[3])

    print area[4]
    if random.randint(0, 1):
        print area[5]
    if random.randint(0, 1) or level == 7:
        print """
        .FARADDR hidden_bonus_object
        .WORD %d
        .BYTE 0
        .WORD %s
        .BYTE 0""" % (random.randint(0, 11), random.choice(hidden_bonuses) if level != 7 else "HEART")
    print """.WORD $F0F0        ; F0F0 marks the end of the init function list
    ; List of enemy create functions"""
    diff = difficulty_for_level(world, level)
    # Extend the pool as the game progresses
    enemy_pool = []
    if diff < 17:
        enemy_pool += easy_enemies[:world * 2]
    if diff > 3 and diff < 19:
        enemy_pool += medium_enemies[:world * 2]
    if diff > 12:
        enemy_pool += hard_enemies[max(world * 2 - 8, 0):world * 2]
    random.shuffle(enemy_pool)
    enemy_pool = enemy_pool[:3] # Each level may only have up to 3 different enemies
    if area[0] == "factory_graphic":
        enemy_pool = enemy_pool[:2] # We can only have 2 enemies in the factory area. This is because moving platforms take one more palette
    if "yoroisu" in [x[1] for x in enemy_pool]:
        enemy_pool = enemy_pool[:2] # We can only have 2 enemies if yoroisu is in use, as it uses too much sprite data.
    while (diff > 0):
        enemy = random.choice(enemy_pool)
        print ".FARADDR create_%s" % (enemy[1])
        diff -= enemy[0]

    print ".WORD 0            ; null terminator"
    n_basic_bonuses = random.randint(1, 2)
    n_special_bonuses = random.randint(0, 1)
    is_first_two_levels = world == 1 and level < 3
    if random.randint(0, 3) == 0 and not is_first_two_levels:
        n_basic_bonuses -= 1
        n_special_bonuses += 1
    elif is_first_two_levels:
        n_special_bonuses = 0
        n_basic_bonuses += 1

    for i in xrange(n_basic_bonuses):
        print ".WORD", random.choice(basic_bonuses)
    for i in xrange(n_special_bonuses):
        print ".WORD", random.choice(special_bonuses[:world * 2])
    while diff < -1.5: # Level is too hard, add difficulty reducing bonuses
        diff += 1
        print ".WORD", random.choice(diff_reduce_bonuses)

    print ".WORD 0            ; null terminator"

def generate_arena_level(world, level):
    print """
            .BYTE $E		; saved_to_d1c
            .BYTE 0
            .BYTE 5			; spawn_and_flags
            .BYTE $80		; $80 here sets a flags that disables "automatic" detection
                            ; of hard block and free spaces tiles, and forces the hard
                            ; coded values of 0804 and 0808. It is used in all stages in
                            ; world 5.
            .WORD 2			; screen_mode
            .WORD $30		; saved_to_d3a
            .FARADDR arena_graphic		; tileset_bank
            .FARADDR bomb_and_explosions_graphic
            .FARADDR empty_tilemap
            .FARADDR arena_level_structure
            .FARADDR empty_tilemap
            .WORD $%x		; level_representation
            .WORD 0			; hard_blocks
            .WORD 0			; soft_blocks
                        ; Off by one in	story mode, for	the level exit
            .FARADDR load_palettes
            .FARADDR arena_palettes
            .WORD $10
            .BYTE 0
            .FARADDR load_global_sprites
            .FARADDR off_C31D6D
            .WORD $10
            .BYTE 0
            .FARADDR loc_C436C1
            .FARADDR locret_C463DD
            .FARADDR tile_animation
            .FARADDR byte_C536D5
            .WORD $20
            .FARADDR tile_animation
            .FARADDR byte_C53716
            .WORD $22
            .FARADDR tile_animation
            .FARADDR byte_C53716+$61
            .WORD $24
            .FARADDR tile_animation
            .FARADDR byte_C537C4
            .WORD $26
            .WORD $F0F0
            .WORD 0
            .WORD 0""" % (world * 0x10 + level, )

# How areas the divided between worlds. This will later be altered to bosses into account
world_areas = [[0,0,0,0,1,1,1,1], [2,2,2,2,3,3,3,3], [4,4,4,5,5,5,6,6], [7,7,7,8,8,9,9,9], [10,10,11,11,11,12,12,12]]
random.shuffle(world_areas)
random.shuffle(areas)
# Todo: we need to modify Dboot banks so crowd sounds will play in the Arena, even if it's not in world 5.
arena_world = random.randint(2, 5) # We don't want the arena world to be the first or last level
print "ARENA_WORLD = %d" % (arena_world)
world_areas.insert(arena_world - 1, None)
for world in xrange(1, 6 + 1):
    for level in xrange(1, 8 + 1):
        print "stage_%d_%d:" % (world, level)
        if world != arena_world:
            generate_random_level(world, level)
        else:
            generate_arena_level(world, level)

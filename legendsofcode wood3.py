import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# constant
DRAFT = True
BATTLE = False
# game loop
while True:
    player = []
    for i in range(2):
        player_health, player_mana, player_deck, player_rune, player_draw = [int(j) for j in input().split()]
        player.append([player_health, player_mana, player_deck, player_rune, player_draw])
        print(player_health, player_mana, player_deck, player_rune, player_draw, file=sys.stderr)

    opponent_hand, opponent_actions = [int(i) for i in input().split()]
    print(opponent_hand, opponent_actions, file=sys.stderr)
    for i in range(opponent_actions):
        card_number_and_action = input()
        print(card_number_and_action, file=sys.stderr)

    player_hand_map = {}
    player_board_map = {}
    opponent_board_map = {}
    card_count = int(input())
    for i in range(card_count):
        inputs = input().split()
        card_number = int(inputs[0])
        instance_id = int(inputs[1])
        location = int(inputs[2])
        card_type = int(inputs[3])
        cost = int(inputs[4])
        attack = int(inputs[5])
        defense = int(inputs[6])
        abilities = inputs[7]
        my_health_change = int(inputs[8])
        opponent_health_change = int(inputs[9])
        card_draw = int(inputs[10])
        print(card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw, file=sys.stderr)
        if location == 0: # Draft phase
            # TODO: key is insatance id to card_number. which is best?
            player_hand_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
        if location == 1:
            player_board_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
        if location == 2:
            opponent_board_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)



    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    if player[0][2] == 29:
        DRAFT = False
        BATTLE = True

    # Draft mode
    if DRAFT:
        print("Draft phase", file=sys.stderr)
        # choose simply most high attack card
        print(player_hand_map, file=sys.stderr)
        attack = 0
        attack_max = 0
        max_id = 0
        # TODO: change card count forin to plyaerhandmap key
        # draft phase instance id is all -1
        for i in range(card_count):
            # BUG:key is not 0, 1, 2,
            attack = player_hand_map[i][5]
            if attack_max <= attack:
                attack_max = attack
                max_id = i
        print("max attack = " + str(attack_max), file=sys.stderr)
        print("PICK", max_id)
        # print("PASS")

    # Battle mode
    if BATTLE:
        print("Battle phase", file=sys.stderr)
        print("PASS")
import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# Wood 2 league
class CardGame():
    def __init__(self):
        # constant
        self.DRAFT = True
        self.BATTLE = False
        self.turn = 0

    def evalDraft(seld, tp_hand, decklist):
        # player_hand_map[card_number] =
        #   (card_number, instance_id, location,
        #   card_type, cost, attack, defense, abilities,
        #   my_health_change, opponent_health_change, card_draw)
        if len(tp_hand) < 11:
            print("hand dict error", file=sys.stderr)
            return -1
        evaluate = 0
        creature_nums = 0
        green_items = 0
        red_items = 0
        blue_items = 0
        CREATURE = 0
        GREEN = 1
        RED = 2
        BLUE = 3


        for card in decklist:
            deck_type = card[3]
            if deck_type == GREEN:
                green_items += 1
            if deck_type == RED:
                red_items += 1
            if deck_type == BLUE:
                blue_items += 1
            if deck_type == CREATURE:
                creature_nums += 1

        card_type, cost, attack, defense = tp_hand[3], tp_hand[4], tp_hand[5], tp_hand[6]
        abilities, my_health_change, opponent_health_change = tp_hand[7], tp_hand[8], tp_hand[9]
        card_draw = tp_hand[10]


        evaluate += attack
        evaluate += defense
        evaluate += my_health_change
        evaluate -= opponent_health_change
        evaluate -= cost
        if len(abilities) < 5:
            print("abilities error", file=sys.stderr)
            return -1

        for s in abilities:
            if s == "-":
                continue
            elif s == "B": # Breakthrough
                evaluate += attack
            elif s == "C": # Charge:summon attack
                evaluate += attack/2 + defense/2
            elif s == "G": # Guard: first guard
                evaluate += defense
            elif s == "D": # Drain:heal player
                evaluate += attack
            elif s == "L": # Lethal:kill
                evaluate += attack
            elif s == "W": # ignore damage
                evaluate += defense


        print("my, opp healthchancge= ", my_health_change, opponent_health_change, file=sys.stderr)

        return evaluate

    def SummonEvaluate(self, card, board, opp_board):
        evalue = 0
        GUARD = False
        for key in board.keys():
            abi = board[key][7] # abilities
            for s in abi:
                if s == "G":
                    GUARD = True
        if not GUARD:
            if "G" in card[7]:
                evalue += card[6]

        return evalue

    def Summon(self, cost, hand, board, opp_board):
        # player_hand_map[instance_id] =
        #   (card_number, instance_id, location, card_type,
        #   cost, attack, defense, abilities, my_health_change,
        #   opponent_health_change, card_draw)
        summon_str = ""
        evalue_max = 0
        maxid = 0
        handcopy = hand.copy()
        print("copysize = ", len(handcopy), len(hand), file=sys.stderr)
        for key in hand.keys():
            evalue = 0
            if cost < hand[key][4]:
                print("cost, cardcost =", cost, hand[key][4], file=sys.stderr)
                handcopy.pop(key)
                print("key del ", key, " copysize = ", len(handcopy), file=sys.stderr)
                continue
            evalue = self.SummonEvaluate(handcopy[key], board, opp_board)
            print("key, evalue = ",key, evalue, file=sys.stderr)
            if evalue >= evalue_max:
                evalue_max = evalue
                maxid = key
        if len(handcopy) > 0:
            summon_str += "SUMMON " + str(maxid) + ";"
            print(handcopy, file=sys.stderr)
            print("evalue:", summon_str, file=sys.stderr)
            return summon_str, maxid

        return summon_str, -1


    def Attack(self, board, opp_board):
        # player_hand_map[instance_id] =
        #   (card_number, instance_id, location, card_type,
        #   cost, attack, defense, abilities, my_health_change,
        #   opponent_health_change, card_draw)
        attack_str = ""
        opp_guard = []
        for key in opp_board.keys():
            if "G" in opp_board[key][7]:
                opp_guard.append(key)
        if len(opp_guard) == 0:
            return attack_str

        opp_id = 0
        for key in board.keys():
            # first, simple attack
            attack_str += "ATTACK " + str(key) + " " + str(opp_guard[opp_id]) + ";"
            if (opp_board[opp_guard[opp_id]][6] - board[key][5]) < 0:
                # opponent defense - my attack
                opp_id += 1
                if len(opp_guard) <= opp_id:
                    break

        return attack_str


    def Run(self):
        print("turn ", self.turn, file=sys.stderr)
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
        player_decklist = []
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
                # NOTE: key is changed insatance id to card_number. which is best?
                if self.DRAFT == True:
                    player_hand_map[card_number] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
                elif self.DRAFT == False and self.BATTLE == False:
                    player_hand_map[card_number] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
                    self.BATTLE = True
                else:
                    player_hand_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)

            if location == 1:
                player_board_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)
            if location == -1:
                opponent_board_map[instance_id] = (card_number, instance_id, location, card_type, cost, attack, defense, abilities, my_health_change, opponent_health_change, card_draw)



        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)

        # Draft mode
        if self.DRAFT:
            print("Draft phase", file=sys.stderr)
            # choose simply most high attack card
            print(player_hand_map, file=sys.stderr)
            #attack = 0
            evalue_max = 0
            max_id = 0
            max_key = 0
            evalue = 0
            # NOTE:changed card count forin to plyaerhandmap key
            # draft phase instance id is all -1
            for i, k in enumerate(player_hand_map.keys()):
                # NOTE:key is not 0, 1, 2,
                evalue = self.evalDraft(player_hand_map[k], player_decklist)
                if evalue_max <= evalue:
                    evalue_max = evalue
                    max_id = i
                    max_key = k

                print("evalue", evalue, file=sys.stderr)
            player_decklist.append(player_hand_map[max_key])

            print("PICK", max_id)
            # print("PASS")

        # Battle mode
        if self.BATTLE:
            print("Battle phase", file=sys.stderr)
            print(player_hand_map, file=sys.stderr)
            print(player_board_map, file=sys.stderr)
            print(opponent_board_map, file=sys.stderr)
            battle_str = ""
            # summon
            cost = player[0][1]
            while cost > 0:
                battle_str_temp, key = self.Summon(cost, player_hand_map, player_board_map, opponent_board_map)
                battle_str += battle_str_temp
                if key == -1:
                    break
                cost -= player_hand_map[key][4] # cost
                player_board_map[key] = player_hand_map[key]
                player_hand_map.pop(key)

            # attack creature
            battle_str += self.Attack(player_board_map, opponent_board_map)

            # attack opponent(-1)
            for id in player_board_map.keys():
                battle_str += "ATTACK " + str(id) + " -1;"

            # action
            if battle_str == "":
                battle_str = "PASS"
            print(battle_str)

        if player[0][2] == 29:
            self.DRAFT = False
            #self.BATTLE = True

        self.turn += 1


# game loop
game = CardGame()
while True:
    game.Run()

import sys
import math
from typing import Awaitable

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
# Wood 2 league
class CardGame():
    def __init__(self):
        # constant
        self.DRAFT = True
        self.BATTLE = False
        self.turn = 0
        self.player_decklist = []

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
        ABLP = 5 # ability point
        cost_list = [0 for i in range(13)]



        for card in decklist:
            deck_type = card[3]
            cost = card[4]
            if deck_type == GREEN:
                green_items += 1
            if deck_type == RED:
                red_items += 1
            if deck_type == BLUE:
                blue_items += 1
            if deck_type == CREATURE:
                creature_nums += 1

            if cost > 12:
                print("cost list index error", file=sys.stderr)
                continue
            cost_list[cost] += 1
        cost_num = [cost_list[i] for i in range(13)]


        card_type, cost, attack, defense = tp_hand[3], tp_hand[4], tp_hand[5], tp_hand[6]
        abilities, my_health_change, opponent_health_change = tp_hand[7], tp_hand[8], tp_hand[9]
        card_draw = tp_hand[10]

        if card_type == GREEN:
            evaluate += 1
        elif card_type == RED:
            evaluate -= attack * 2
            evaluate -= defense * 2
        elif card_type == BLUE:
            evaluate -= defense * 2

        if len(decklist) > 15:
            if card_type == GREEN and (green_items < 3):
                evaluate += 10
            elif card_type == RED and (red_items < 2):
                evaluate += 10
            elif card_type == BLUE and (blue_items < 2):
                evaluate += 10

        if card_type == CREATURE and (cost < 4 ) and (cost_num[cost] < 4):
            evaluate += 5

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
                evaluate += ABLP
            elif s == "C": # Charge:summon attack
                evaluate += attack/2 + defense/2
                evaluate += ABLP
            elif s == "G": # Guard: first guard
                evaluate += defense
                evaluate += ABLP
            elif s == "D": # Drain:heal player
                evaluate += attack
                evaluate += ABLP
            elif s == "L": # Lethal:kill
                evaluate += attack
                evaluate += ABLP
            elif s == "W": # ignore damage
                evaluate += defense
                evaluate += ABLP


        # print("my, opp healthchancge= ", my_health_change, opponent_health_change, file=sys.stderr)

        return evaluate


    def PrintDeckType(self, decklist):
        print("len(decklist) = ", len(decklist), file=sys.stderr)
        creature_nums = 0
        green_items = 0
        red_items = 0
        blue_items = 0
        CREATURE = 0
        GREEN = 1
        RED = 2
        BLUE = 3
        cost_list = [0 for i in range(13)]

        for card in decklist:
            deck_type = card[3]
            cost = card[4]
            if deck_type == GREEN:
                green_items += 1
            if deck_type == RED:
                red_items += 1
            if deck_type == BLUE:
                blue_items += 1
            if deck_type == CREATURE:
                creature_nums += 1
                if cost > 12:
                    print("cost list index error", file=sys.stderr)
                    continue
                cost_list[cost] += 1

        cost_num = [cost_list[i] for i in range(13)]
        print("C:", file=sys.stderr, end="")
        print("+" * (creature_nums//5), "*" * (creature_nums % 5), file=sys.stderr)
        print("G:", file=sys.stderr, end="")
        print("*" * (green_items), file=sys.stderr)
        print("R:", file=sys.stderr, end="")
        print("*" * (red_items), file=sys.stderr)
        print("B:", file=sys.stderr, end="")
        print("*" * (blue_items), file=sys.stderr)
        for i in range(13):
            print(str(i)+":", file=sys.stderr, end="")
            print("+" * (cost_num[i] // 5) + "*" * (cost_num[i] % 5), file=sys.stderr)


        return 0




    def SummonEvaluate(self, card, board, opp_board):
        """when summon, evaluate summon efficient value

        Args:
            card (dict): [description]
            board (dict): [description]
            opp_board (dict): [description]

        Returns:
            dict: [description]
        """
        # player_hand_map[instance_id] =
        #   (card_number, instance_id, location, card_type,
        #   cost, attack, defense, abilities, my_health_change,
        #   opponent_health_change, card_draw)
        evalue = 0
        GUARD = False
        for key in board.keys():
            abi = board[key][7] # abilities
            for s in abi:
                if s == "G":
                    GUARD = True
        if not GUARD:
            if "G" in card[7]:
                evalue += card[6] # defense

        if len(board) > 2:
            if card[3] == 1: # card type == GREEN
                evalue += 5


        return evalue

    def Summon(self, cost, hand, board, opp_board):
        # player_hand_map[instance_id] =
        #   (card_number, instance_id, location, card_type,
        #   cost, attack, defense, abilities, my_health_change,
        #   opponent_health_change, card_draw)
        summon_str = ""
        evalue_max = 0
        maxid = -1
        handcopy = hand.copy()
        # print("copysize = ", len(handcopy), len(hand), file=sys.stderr)
        for key in hand.keys():
            evalue = 0
            if cost < hand[key][4]: # ignore if player cost < card cost
                # print("cost, cardcost =", cost, hand[key][4], file=sys.stderr)
                handcopy.pop(key)
                # print("key del ", key, " copysize = ", len(handcopy), file=sys.stderr)
                continue
            evalue = self.SummonEvaluate(handcopy[key], board, opp_board)
            print("key, evalue = ",key, evalue, file=sys.stderr)
            if evalue >= evalue_max:
                evalue_max = evalue
                maxid = key

        if len(handcopy) > 0:
            if hand[maxid][3] == 0: # CREATURE
                summon_str += "SUMMON " + str(maxid) + ";"
            elif hand[maxid][3] == 1: # GREEN
                cost_temp = 0
                cost_max = 0
                cost_maxid = -1
                for key in handcopy.keys():
                    cost_temp = handcopy[key][4]
                    if cost_temp >= cost_max:
                        cost_max = cost_temp
                        cost_maxid = key

                summon_str += "USE " + str(maxid) + " " + str(cost_maxid) + ";"

            elif hand[maxid][3] == 2: # RED
                if len(opp_board) == 0:
                    summon_str = ""
                    maxid = -1
                elif len(opp_board) > 0:
                    cost_temp = 0
                    cost_max = 0
                    cost_maxid = -1
                    for key in opp_board.keys():
                        cost_temp = opp_board[key][4]
                        if cost_temp >= cost_max:
                            cost_max = cost_temp
                            cost_maxid = key

                    summon_str += "USE " + str(maxid) + " " + str(cost_maxid) + ";"

            elif hand[maxid][3] == 3: # BLUE
                summon_str += "USE " + str(maxid) + " " + "-1;"
            # print(handcopy, file=sys.stderr)
            # print("evalue:", summon_str, file=sys.stderr)

        return summon_str, maxid


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
            _ = self.PrintDeckType(self.player_decklist)
            #attack = 0
            evalue_max = 0
            max_id = 0
            max_key = 0
            evalue = 0
            # NOTE:changed card count forin to plyaerhandmap key
            # draft phase instance id is all -1
            for i, k in enumerate(player_hand_map.keys()):
                # NOTE:key is not 0, 1, 2,
                evalue = self.evalDraft(player_hand_map[k], self.player_decklist)
                if evalue_max <= evalue:
                    evalue_max = evalue
                    max_id = i
                    max_key = k

                print("evalue", evalue, file=sys.stderr)
            # print("decklist append:", player_hand_map[max_key], file=sys.stderr)
            self.player_decklist.append(player_hand_map[max_key])

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

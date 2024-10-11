import os
import random
round = 0
CurrentBet = 0
Pot = 0
game = True
FirstTurn = True
Hand_Value = ['High Card', 'One Pair', 'Two Pair', 'Three of a kind', 'Straight', 'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']
class Hand:  # class Defining what a hand is, this isn't really necessary I just wanted to include it to cement my knowldedge
    def __init__(self):
        self.Hand = []
        self.best_case = self.CalcValue()
    def hand_to_string(self):
        output = []
        for card in self.Hand:
            output.append(f'{card.Name} of {card.Suit}')
        return ', '.join(output)
class Player(Hand):  # class for each player, inheriting from Hand because why not
    def __init__(self, aName, aWallet):  # Player class requires a name
        super().__init__()
        self.Name = aName
        self.Wallet = aWallet
        self.Folded = False
        self.lastMove = ''
    def Call(self):
        global Pot, CurrentBet
        self.Wallet -= CurrentBet
        Pot += CurrentBet
        CurrentBet += CurrentBet
        self.lastMove = 'Call'
    def Fold(self):
        self.Folded = True
        self.lastMove = 'Fold'
    def Raise(self):
        global Pot, CurrentBet
        try:
            tempInt = int(input('How much would you like to raise?\n'))
            if tempInt > self.Wallet or tempInt < 5 or tempInt < CurrentBet:
                raise ValueError
        except ValueError:
            print(f'Your input is outside of the scope of your funds or below the minimum raise value(5)')
            return self.Raise(self)
        CurrentBet += tempInt
        self.Wallet -= CurrentBet
        Pot += CurrentBet
        self.lastMove = f'Raise {CurrentBet}'
    def Bet(self):
        global Pot, CurrentBet
        try:
            tempInt = int(input('How much would you like to bet?\n'))
            if tempInt > self.Wallet or tempInt < 5:
                raise ValueError
        except ValueError:
            print(f'Your input is outside of the scope of your funds or below the minimum bet value(5)')
            return self.Bet(self)
        CurrentBet = tempInt
        self.Wallet -= tempInt
        Pot += tempInt
        self.lastMove = f'Bet {tempInt}'
    def CalcValue(self):
        if has_royal_flush(self) == True:
            return 9
        elif has_straight_flush(self) == True:
            return 8
        elif has_4_of_kind(self) == True:
            return 7
        elif has_full_house(self) == True:
            return 6
        elif has_flush(self) == True:
            return 5
        elif has_straight(self) == True:
            return 4
        elif has_3_of_a_kind(self) == True:
            return 3
        elif isinstance(has_2_of_a_kind(self), list):
            if len(has_2_of_a_kind(self)) == 2:
                return 2
            elif len(has_2_of_a_kind(self)) == 1:
                return 1
        else:
            return 0
    def reset(self):
        self.__init__()
    def __del__(self):
        return
class Card:
    def __init__(self, aName, aSuit, aWeight):
        self.Name = aName
        self.Suit = aSuit
        self.Weight = aWeight
    def card_2string(self):
        result = f'{self.Name} of {self.Suit}'
        return result
    def AceValue(self, context):
        if context == 'high':
            return 14
        if context == 'low':
            return 1
class Deck(): #Deck class because it's more organized to have everything together
    def __init__(self):
        self.deck = self.render()
        self.Top = 51
    def render(self):
        output = []
        suits = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
        names = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        weights = [Card.AceValue(self, 'high'), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        for suit in suits:
            for name, weight in zip(names, weights):
                output.append(Card(name, suit, weight))
        return output
    def shuffle(self):
        i = 0
        while i < 11:
            random.shuffle(self.deck)
            i+=1
        return deck
    def deal(self, aPlayer):
        aPlayer.Hand.append(self.deck[self.Top])
        self.Top -= 1
    def reset(self):
        self.__init__()
    def stringify(self):
        output = ''
        for card in self.deck:
            output += " ".join(self.deck[card])
            output += "\n"
        return output
def calc_winner():
    top_value = max(player.CalcValue() for player in Players if not player.Folded)
    contenders = [player for player in Players if player.CalcValue() == top_value and not player.Folded]
    if len(contenders) > 1:
        high_card_values = [high_card(player) for player in contenders]
        max_high_card = max(high_card_values)
        winner_index = high_card_values.index(max_high_card)
        return contenders[winner_index]
    else:
        return contenders[0]
def initialize_players():
    try:
        Players_in = input('Please input the names of the players: (E.g Player1 Player2)\n')
        if 1 < len(Players_in.split(" ")) > 5:
            raise ValueError
    except ValueError:
        print("There must be 1-5 players")
        return initialize_players()
    if Players_in == 'exit' or 'e' or "":
        game = False
    Players = []
    for name in Players_in.split(" "):
        Players.append(Player(name, 100))
    return Players
def display_hands(IntArg):
    for player in len(Players):
        print(f'{player.Name}  has {player.hand_to_string()}')
'''def of_a_kind(aPlayer): # check
    maxcomp = [(for card in player.Hand if player.count(card.weight) > 1)]
    return maxcomp'''   #I don't really see the point of this but I wrote it
def compare():
    ToCompare = [player for player in Players if player.Folded == False]
    return ToCompare
def high_card(aPlayer): #highest value
    result = 0
    for card in aPlayer.Hand:
        if card.Name == 'Ace':
            result += card.AceValue('high')
        else:
            result += card.Weight
    return result
def has_2_of_a_kind(aPlayer):
    name_counts = {}
    for card in aPlayer.Hand:
        if card.Name in name_counts:
            name_counts[card.Name] += 1
        else:
            name_counts[card.Name] = 1
    pairs = [card_name for card_name, count in name_counts.items() if count == 2]
    if len(pairs) > 0:
        return pairs
    else:
        return False
def has_3_of_a_kind(aPlayer): # 3 same type
    names = [card for card in aPlayer.Hand if card.Name]
    for name in set(names):
        if names.count(name) == 3:
            return True
    return False
def has_straight(aPlayer):
    if len(aPlayer.Hand) < 5:
        return False
    weights = sorted([card.Weight for card in aPlayer.Hand])
    for i in range(len(weights) - 4):
        if weights[i] + 1 == weights[i + 1] and weights[i + 1] + 1 == weights[i + 2] and weights[i + 2] + 1 == weights[
            i + 3] and weights[i + 3] + 1 == weights[i + 4]:
            return True
    if weights[-1] == 14 and weights[0] == 2 and weights[1] == 3 and weights[2] == 4 and weights[3] == 5:
        return True
    return False
def has_flush(aPlayer): # 5 cards same Suit
    if len(aPlayer.Hand) < 5:
        return False
    flush_test = [card == Card for card in aPlayer.Hand if card.Name]
    for name in flush_test:
        if flush_test.count(name) == 5:
            return True
    return False
def has_full_house(aPlayer): # 3 of a kind + 2 of a kind
    if has_2_of_a_kind(aPlayer) != False:
        if len(has_2_of_a_kind(aPlayer)) == 2:
            if has_3_of_a_kind(aPlayer) != False:
                return True
            else:
                return False
    else:
        return False
def has_4_of_kind(aPlayer):# 4 same type
    if len(aPlayer.Hand) < 4:
        return False
    FourOfCheck = [card for card in aPlayer.Hand if card.Name]
    for name in FourOfCheck:
        if FourOfCheck.count(name) == 4:
            return True
    return False
def has_straight_flush(aPlayer): # 5 same type
    if has_flush(aPlayer) == True and has_straight(aPlayer) == True:
        return True
    else:
        return False
def has_royal_flush(aPlayer): # 10-ace same type
    if has_flush(aPlayer) == True and high_card(aPlayer) == 60:
        return True
    else:
        return False
def turn(aPlayer):
    global FirstTurn
    if FirstTurn == False:
        for player in Players:
            if player.Name != aPlayer.Name:
                print(f'{player.Name}\'s last move was {player.lastMove}')
    if aPlayer.Folded == False:
        if FirstTurn == True:
            try:
                if aPlayer.CalcValue() == 0:
                    Decision = input(f'Current Pot: {Pot}\nCurrent Bet: {CurrentBet}\n{aPlayer.Name} has {aPlayer.hand_to_string()}\nThis is a High card of {high_card(aPlayer)}\nWould you like to Check Fold or Bet\n')
                else:
                    Decision = input(f'Current Pot: {Pot}\nCurrent Bet: {CurrentBet}\n{aPlayer.Name} has {aPlayer.hand_to_string()}\nThis is a {Hand_Value[aPlayer.CalcValue()]}\nWould you like to Check Fold or Bet\n')
                if Decision.lower() != 'check' and Decision.lower() != 'bet' and Decision.lower() != 'fold':
                    raise ValueError
            except ValueError:
                print('There was an error with your input')
                return turn(aPlayer)
            if Decision.lower() == 'bet':
                aPlayer.Bet()
            elif Decision.lower() == 'check':
                print('You Checked')
                aPlayer.lastMove = 'Checked'
            elif Decision.lower() == 'fold':
                aPlayer.Fold()
            FirstTurn = False
        else:
            try:
                if aPlayer.CalcValue() == 0:
                    Decision = input(f'Current Pot: {Pot}\nCurrent Bet: {CurrentBet}\n{aPlayer.Name} has {aPlayer.hand_to_string()}\nThis is a High card of {high_card(aPlayer)}\nWould you like to Call, Check, Fold or Raise\n')
                else:
                    Decision = input(f'Current Pot: {Pot}\nCurrent Bet: {CurrentBet}\n{aPlayer.Name} has {aPlayer.hand_to_string()}\nThis is a {Hand_Value[aPlayer.CalcValue()]}\nWould you like to Call, Check, Fold or Raise\n')
                if Decision.lower() != 'check' and Decision.lower() != 'raise' and Decision.lower() != 'fold' and Decision.lower() != 'call':
                    raise ValueError
            except ValueError:
                print('There was an error with your input')
                return turn(aPlayer)
            if Decision.lower() == 'raise':
                aPlayer.Raise()
            elif Decision.lower() == 'check':
                aPlayer.lastMove = 'Checked'
            elif Decision.lower() == 'call':
                aPlayer.Call()
            elif Decision.lower() == 'fold':
                aPlayer.Fold()
        print(f'You {aPlayer.lastMove}')
        os.system('cls')
        print('Please allow the next player to fulfill their turn')
        os.system('pause')
''''def player_leave(aPlayer):
    for player in Players:
        if player.Name == aPlayer:
            player.__del__()'''
def reset():
    round = 0
    Pot = 0
    CurrentBet = 0
    FirstTurn = True
def CanContQuery():
    PwithM = [player for player in Players if player.Wallet > 0]
    if len(PwithM) > 1:
        return True
    else:
        return False
def Gaming():
    global round
    for player in Players:
        deck.deal(player)
    while (round < 3) and (len(Players) > 1) and (len(compare()) > 1):
        for player in Players:
            deck.deal(player)
        for player in Players:
            if player.Folded == False:
                turn(player)
        round += 1
    if round > 1:
        print(
            f'{calc_winner().Name} has won with a {Hand_Value[calc_winner().CalcValue()]}\n{calc_winner().hand_to_string()}')
    if CanContQuery() == True:
        reset()
        return Gaming()
if __name__ == '__main__': #Wallet functionality has not been added
    deck = Deck()
    deck.shuffle()
    iteration = 0
    while game == True:
        if iteration == 0:
            Players = initialize_players()
            Gaming()
        else:
            try:
                continuequery = input('Would you like to continue playing with these players? (e or exit to exit)\n')
                if continuequery.lower() == 'yes' or continuequery.lower() == 'y':
                    reset()
                    gaming()
                elif continuequery.lower() == 'no' or continuequery.lower() == 'n':
                    Players = initialize_players()
                    Gaming()
                elif continuequery.lower() == 'e' or continuequery.lower() == 'exit' or continuequery == '':
                    game = False
                else:
                    raise ValueError
            except ValueError:
                print('Please be sure to input the correct value')
        iteration += 1
    print("Thanks for playing!")
    os.system('pause')
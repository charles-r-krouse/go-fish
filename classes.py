import random


class Card:
    def __init__(self, strength, suit):
        self.strength = strength
        self.suit = suit
        ranks = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8,
                 9: 9, 10: 10, 11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}
        self.rank = ranks.get(self.strength)

    def __repr__(self):
        return '({} of {})'.format(self.rank, self.suit)


class Deck:
    def __init__(self):
        self.cards = []
        values = range(2, 15)
        suits = ['HEARTS', 'DIAMONDS', 'CLUBS', 'SPADES']
        for suit in suits:
            for value in values:
                self.cards.append(Card(suit=suit, strength=value))

    def __repr__(self):
        return '{} card deck created.'.format(len(self.cards))

    def __iter__(self):
        for card in self.cards:
            yield card

    def shuffle(self):
        return random.shuffle(self.cards)

    def deal(self, num_cards=7):
        # assume the cards are already shuffled
        for card in range(0, num_cards):
            for player in Player.instances:
                player.add_card_to_hand(self.cards[0])
                self.remove_card(self.cards[0])

    def remove_card(self, card):
        self.cards.remove(card)


class Player:
    instances = []

    def __init__(self, name: str):
        self.name = name
        self.hand = []
        self.score = 0
        Player.instances.append(self)

    def __repr__(self):
        return 'Player: {}'.format(self.name)

    def view_hand(self):
        print("{}'s cards:".format(self.name))
        sorted_hand = sorted(self.hand, key=lambda x: x.strength)
        self.hand = sorted_hand
        for card in sorted_hand:
            print('>> {}'.format(card, end='\n'))
        return ''

    def add_card_to_hand(self, card: Card):
        self.hand.append(card)

    def remove_card_from_hand(self, card: Card):
        self.hand.remove(card)

    def draw_card(self, deck: Deck):
        if len(deck.cards) == 0:
            return None
        new_card = deck.cards[0]
        self.add_card_to_hand(new_card)
        deck.remove_card(new_card)
        return new_card

    def ask_for_a_card(self, opponent=None):
        return random.choice(self.hand)

    def ask_an_opponent(self):
        while True:
            opponent = random.choice(Player.instances)
            if opponent.name != self.name and len(opponent.hand) != 0:
                break
        return opponent


class HumanPlayer(Player):
    def ask_an_opponent(self):
        # TODO: error handling for invalid entry
        print('Available players:')
        available_players = []
        for p in Player.instances:
            if p.name == self.name:
                continue
            else:
                available_players.append(p)
        for index, p in enumerate(available_players):
            print('{} - {}'.format(index+1, p.name))
        selection = input('Who do you want to ask?\n')
        if not selection.isnumeric():
            print('Invalid entry. Please enter a number.')
            self.ask_an_opponent()
        selection = int(selection) - 1
        if selection in range(0, len(available_players)):
            return (available_players[selection])
        else:
            print('Invalid selection. Please select a different player.')
            self.ask_an_opponent()

    def get_entry(self, players):
        selection = input('Who do you want to ask?\n')
        if not selection.isnumeric():
            print('Invalid entry. Please enter a valid number.')

    def ask_for_a_card(self, opponent=None):
        # TODO: error handling for invalid entry
        print('Your cards:')
        for index, card in enumerate(self.hand):
            print('{} - {}'.format(index + 1, card))
        selection = input('What card do you want to ask {} for?\n'.format(opponent.name))
        selection = int(selection) - 1
        return self.hand[selection]

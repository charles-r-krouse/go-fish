from classes import *


def play_go_fish(deck: Deck):
    # TODO: add a known history for the AI so that the AI knows what cards other players have asked for
    # TODO: after debugging... move all print() statements to the main loop
    turn = 1
    game_over = False
    while game_over == False:
        print('\n********* Start of turn {} *********'.format(turn))
        print('The deck: {} cards - {}'.format(len(deck.cards), deck.cards))
        search_for_existing_pairs()
        # use a 'break' command to exit the loop
        for player in Player.instances:
            match = True
            # it remains the player's turn until he doesn't get a match
            print("\n{}'s turn:".format(player.name))
            while match == True:
                if len(player.hand) == 0:
                    draw_new_hand(player, deck)
                if len(player.hand) == 0:
                    print('No cards remaining to draw.')
                    break
                desired_opponent = player.ask_an_opponent()
                print('...DESIRED OPPONENT = {}'.format(desired_opponent))
                desired_card = player.ask_for_a_card(desired_opponent)
                print('{} asks {} for a {}...'.format(
                    player.name, desired_opponent.name, desired_card.rank))
                # loop until the player asks an opponent for a card that he doesn't have
                match = determine_if_there_is_a_match(player, desired_opponent, desired_card, deck)
            print("End of {}'s turn.".format(player.name))
        print('********* End of turn {} *********'.format(turn))
        for p in Player.instances:
            p.view_hand()
        turn += 1
        if (len(deck.cards)) == 0:
            for p in Player.instances:
                if len(p.hand) == 0:
                    print('Finally, {} has no cards in his hand. GAME OVER.'.format(p.name))
                    game_over = True


def determine_play_order(deck: Deck):
    deck.deal(1)
    Player.instances = sorted(Player.instances, key=lambda x: x.hand[0].strength, reverse=True)
    for p in Player.instances:
        p.remove_card_from_hand(p.hand[0])
    deck.__init__()
    deck.shuffle()


def determine_if_there_is_a_match(player, desired_opponent, desired_card, deck):
    for x in desired_opponent.hand:
        if x.rank == desired_card.rank:
            player.score += 1
            player.remove_card_from_hand(desired_card)
            desired_opponent.remove_card_from_hand(x)
            print('Match!')
            print('{} has a {} and {} has a {}.'.format(player.name, desired_card, desired_opponent.name, x))
            return True
    print('{} does not have a {}.'.format(desired_opponent.name, desired_card.rank))
    if len(deck.cards) != 0:
        fishing_card = player.draw_card(deck)
        print('{} draws a card. It is a {}.'.format(player.name, fishing_card))
    else:
        fishing_card = None
        print('{} cannot draw a card. There are zero cards left in the deck.'.format(player.name))
    if fishing_card and fishing_card.rank == desired_card.rank:
        print('How lucky! {} drew a {}!'.format(player.name, fishing_card))
        player.score += 1
        player.remove_card_from_hand(desired_card)
        player.remove_card_from_hand(fishing_card)
        return True
    return False


def search_for_existing_pairs():
    for player in Player.instances:
        print("Examining {}'s hand...".format(player.name))
        # TODO: improve this - too many nested loops
        for c1 in player.hand:
            for c2 in player.hand:
                if c1 != c2 and c1.rank == c2.rank:
                    print('Lucky! {} was dealt a match of {}s!'.format(player.name, c1.rank))
                    player.remove_card_from_hand(c1)
                    player.remove_card_from_hand(c2)
                    player.score += 1


def draw_new_hand(player, deck):
    num_cards = 5
    if len(deck.cards) < num_cards:
        num_cards = len(deck.cards)
    for _ in range(0, num_cards):
        player.draw_card(deck)
    print('{} draws {} new cards.'.format(player.name, num_cards))


def determine_winner():
    # TODO: consider a 3-way tie
    winner = max(Player.instances, key=lambda x: x.score)
    for player in Player.instances:
        if player != winner and player.score == winner.score:
            return winner.name, player.name
    return winner.name,

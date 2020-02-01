from game_mechanics import *

def main():
    # create a deck of cards
    d = Deck()
    d.shuffle()

    # create some players
    charles = HumanPlayer('Charles')
    # charles = Player('Charles')
    danny = Player('Danny')
    # ben = Player('Ben')
    dad = Player('Dad')

    print('Determining player order...')
    determine_play_order(d)

    # for i in d: print(i,end=',')
    # print()
    d.deal(3)
    # for i in d: print(i,end=',')
    # print()
    print('Starting hands...')
    for p in Player.instances:
        p.view_hand()

    # charles.draw_card(d)
    # ben.draw_card(d)
    # charles.view_hand()
    # for i in d: print(i,end=',')

    play_go_fish(d)

    print()
    print('Finished hands...')
    # for i in d: print(i,end=',')
    print()
    for p in Player.instances:
        p.view_hand()
    print('\nFinal scores:')
    for p in Player.instances:
        print("{}'s score = {}".format(p.name, p.score))

    winner = determine_winner()
    print()
    if len(winner) > 1:
        print('Tie game between {} and {}.'.format(winner[0].upper(), winner[1].upper()))
    else:
        print('Congratulations {}!! You win!'.format(winner[0].upper()))

if __name__ == '__main__':
    main()

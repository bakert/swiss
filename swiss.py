# Swiss tournament pairings
# © 2018 Thomas David Baker <bakert@gmail.com>
# MIT License

# Blossom algorithm implementation from http://jorisvr.nl/article/maximum-matching
# Practical application gleaned from https://www.leaguevine.com/blog/18/swiss-tournament-scheduling-leaguevines-new-algorithm/
# Weighting for Magic tournaments developed after discussion with the good folks of https://pennydreadfulmagic.com/

from collections import Counter
import itertools
import sys

import mwmatching

# EXAMPLE

def example():
    # A player or team is represented by a dict with 'id': <any>, 'points': <number> and 'opponents': [<id>,  …] key-value pairs.
    # If there is an odd number of players the bye should be passed in explicitly so that the system knows which players have previously received the bye ('opponents').
    # Here is an example of pairing the second round of a tournament at the end of the first round.

    players = [
        {'id': 'Abimbola',  'points': 3, 'opponents':  ['Boipelo'] },
        {'id': 'Boipelo',  'points': 0, 'opponents':  ['Abimbola'] },
        {'id': 'Chiamaka', 'points': 1, 'opponents':  ['Delo'] },
        {'id': 'Delo', 'points': 1, 'opponents': ['Chiamaka']},
        {'id': 'Ebele', 'points':  0, 'opponents': ['Furaha']},
        {'id': 'Furaha', 'points':  3, 'opponents': ['Ebele']},
        {'id': 'Zula', 'points':  3, 'opponents': ['BYE']},
        {'id': 'BYE', 'points':  0, 'opponents': ['Zula']},
    ]

    # Where more than one set of pairings is optimal the code will always return one deterministic set.
    # To avoid something like signup order affecting pairings you may wish to randomize the participants first.

    # from random import shuffle
    # shuffle(players)

    ps = pairings(players) # [3, 4, 7, 0, 1, 6, 5, 2] in the unshuffled case

    # Entries in `ps` are for the corresponding participant in `players` and the value is the index in `players` of their opponent.
    # players[0] should play against players[ps[0]]
    # players[1] should play against players[ps[1]]
    # players[2] should play against players[ps[2]]
    # and so on

    for i in range(0, len(ps)):
        if players[i]:
            p1 = players[i]
            p2 = players[ps[i]]
            print("{id1} ({pts1}) v {id2} ({pts2})".format(id1=p1['id'], pts1=p1['points'], id2=p2['id'], pts2=p2['points']))
            players[ps[i]] = None # Don't print this pairing again when we see it from the other player's perspective.

def pairings(players):
    ws = weights(players)
    ps = mwmatching.maxWeightMatching(ws)
    assert(-1 not in ps) # maxWeightMatching is happy to leave nodes out if the graph is maximal, but we are not. Fail early in such a case.
    return ps

def weights(players):
    highest_points = max([p['points'] for p in players])
    ws = []
    for i in range(0, len(players)):
        for j in range(0, len(players)):
            if i == j:
                break
            ws.append((i, j, weight(highest_points, players[i], players[j])))
    return ws

def weight(highest_points, p1, p2):
    w = 0

    # A pairing where the participants have not played each other as many times as they have played at least one other participant outscore all pairings where the participants have played the most times.
    # This will stave off re-pairs and second byes for as long as possible, and then re-re-pairs and third byes, and so on …
    counter = Counter(p1['opponents'])
    if len(counter) > 0 and counter.get(p2['id'], sys.maxsize) < max(counter.values()):
        w += quality(highest_points, highest_points) + 1

    # Determine a score for the quality of this pairing based on the points of the higher scoring participant of the two (importance) and how close the two participants records are.
    best = max(p1['points'], p2['points'])
    worst = min(p1['points'], p2['points'])
    spread = best - worst
    closeness = highest_points - spread
    importance = best
    w += quality(importance, closeness)

    return w

# importance and closeness are values in the range 0..highest_points
def quality(importance, closeness):
    # We add one to these values to avoid sometimes multiplying by zero and losing information.
    return (importance + 1) * (closeness + 1)

if __name__ == '__main__':
    example()

# Run tests with `python3 swiss_test.py`.

import swiss
import unittest

class TestSwiss(unittest.TestCase):
    def players(self):
        return [
            {'id': 'Abimbola',  'points': 3, 'opponents':  ['Boipelo'] },
            {'id': 'Boipelo',  'points': 0, 'opponents':  ['Abimbola'] },
            {'id': 'Chiamaka', 'points': 1, 'opponents':  ['Delo'] },
            {'id': 'Delo', 'points': 1, 'opponents': ['Chiamaka']},
            {'id': 'Ebele', 'points':  0, 'opponents': ['Furaha']},
            {'id': 'Furaha', 'points':  3, 'opponents': ['Ebele']},
            {'id': 'Zula', 'points':  3, 'opponents': ['BYE']},
            {'id': 'BYE', 'points': 0, 'opponents': ['Zula']},
        ]

    def test_pairings(self):
        ps = swiss.pairings(self.players())
        self.assertEqual('Delo', self.players()[ps[0]]['id'])
        self.assertEqual('Ebele', self.players()[ps[1]]['id'])
        self.assertEqual('BYE', self.players()[ps[2]]['id'])
        self.assertEqual('Abimbola', self.players()[ps[3]]['id'])
        self.assertEqual('Boipelo', self.players()[ps[4]]['id'])
        self.assertEqual('Zula', self.players()[ps[5]]['id'])
        self.assertEqual('Furaha', self.players()[ps[6]]['id'])
        self.assertEqual('Chiamaka', self.players()[ps[7]]['id'])

    def test_weights(self):
        ws = swiss.weights(self.players())
        self.assertEqual((1, 0, 4), ws[0])
        self.assertEqual((2, 0, 8), ws[1])
        self.assertEqual((2, 1, 6), ws[2])
        self.assertEqual((3, 0, 8), ws[3])
        self.assertEqual((3, 1, 6), ws[4])
        self.assertEqual((3, 2, 8), ws[5])
        self.assertEqual((4, 0, 4), ws[6])

    def test_weight(self):
        highest_points = max(p['points'] for p in self.players())
        w = swiss.weight(highest_points, self.players()[0], self.players()[1])
        self.assertEqual(4, w)
        w = swiss.weight(highest_points, self.players()[1], self.players()[2])
        self.assertEqual(6, w)
        w = swiss.weight(highest_points, self.players()[0], self.players()[7])
        self.assertEqual(4, w)

    # importance and closeness are values in the range 0..highest_points
    def test_quality(self):
        self.assertEqual(6, swiss.quality(1, 2))
        self.assertEqual(6, swiss.quality(2, 1))
        self.assertEqual(12, swiss.quality(3, 2))
        self.assertEqual(4, swiss.quality(3, 0))
        self.assertEqual(26, swiss.quality(12, 1))

if __name__ == '__main__':
    unittest.main()

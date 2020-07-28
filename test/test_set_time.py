from unittest import TestCase
from openeew.set_time import set_time


class SetTimeTest(TestCase):
    def test_with_two_times(self):
        times = [1595951432794, 1595951443718]
        sample_rate = 0.5
        samples = 2
        expected = [1595951421870, 1595951432794, 1595951443718]
        actual = set_time(times, sample_rate, samples)
        self.assertEquals(expected, actual)

    def test_with_one_time(self):
        times = [1595951432794]
        sample_rate = 0.5
        samples = 1
        expected = [1595951432792, 1595951432794, 1595951432796]
        actual = set_time(times, sample_rate, samples)
        self.assertEquals(expected, actual)

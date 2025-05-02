import unittest


def reverse(s):
    if type(s) != str:
        raise TypeError('Expected str, got {}'.format(type(s)))

    return s[::-1]


class TestReverse(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(reverse(''), '')
        self.assertEqual(reverse('a'), 'a')
        self.assertEqual(reverse('aba'), 'aba')
        self.assertEqual(reverse('abc'), 'cba')

    def test_wrong_type(self):
        with self.assertRaises(TypeError):
            reverse(42)
        with self.assertRaises(TypeError):
            reverse(['a', 'b', 'c'])


if __name__ == '__main__':
    unittest.main()

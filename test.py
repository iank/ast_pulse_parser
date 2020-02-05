import pulse
import unittest

class ParseTest(unittest.TestCase):
    def test_pulse(self):
        self.assertEqual(pulse.fun(3), 5)

if __name__ == '__main__':
    unittest.main()

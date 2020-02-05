import pulse
import unittest
import numpy as np

class ParseTest(unittest.TestCase):
    def test_pulse_equality(self):
        self.assertEqual([pulse.Pulse(1, 2)], [pulse.Pulse(1, 2)])

    def test_simple_pulse(self):
        text = "pulse(3, 2)"
        self.assertEqual(pulse.parse(text), [pulse.Pulse(3, 2)])

    def test_pulse_with_np(self):
        text = "pulse(3, np.linspace(0, 10, 10)[4])"
        self.assertEqual(pulse.parse(text), [pulse.Pulse(3, np.linspace(0, 10, 10)[4])])

    def test_sum_of_pulses(self):
        text = "pulse(3, 2) + pulse(1, 4) + pulse(3, 8)"
        self.assertEqual(pulse.parse(text), [
            pulse.Pulse(3, 2),
            pulse.Pulse(1, 4),
            pulse.Pulse(3, 8),
        ])

    def test_sum_of_pulses_with_parens(self):
        """This changes the form of the top level BinOp.."""
        text = "(pulse(3, 2) + pulse(1, 4)) + pulse(3, 8)"
        self.assertEqual(pulse.parse(text), [
            pulse.Pulse(3, 2),
            pulse.Pulse(1, 4),
            pulse.Pulse(3, 8),
        ])


    def test_pulse_with_complex_args(self):
        text = "pulse(3, sum([1, 2*3-5]))"
        self.assertEqual(pulse.parse(text), [pulse.Pulse(3, 2)])

if __name__ == '__main__':
    unittest.main()

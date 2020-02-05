import pulse
import unittest

class ParseTest(unittest.TestCase):
    def test_pulse_equality(self):
        self.assertEqual([pulse.Pulse(1, 2)], [pulse.Pulse(1, 2)])

    def test_simple_pulse(self):
        text = "pulse(3, 2)"
        self.assertEqual(pulse.parse(text), [pulse.Pulse(3, 2)])

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

{'Amplitude': 'Amplitude'}


'pulse(0.10, 0.500, Amplitude)' -> [(0.10, 0.500, 'Amplitude')]
'pulse(0.01, 0.01, 10*mV) + \npulse(\n  times=0.1 + np.linspace(0, 0.01 * (10-1), 10),\n  widths=0.005,\n  values=20*mV\n) + \npulse(0.25, 0.014, Pulse2_amplitude)'
        ->[(0.01, 0.01, 0.01), ([0.1 , 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19], 0.005, 0.02), (0.25, 0.014, 'Pulse2_amplitude')]
'pulse(widths=0.01, times=[0.1,0.2,0.3], values=30*mV)' -> [([0.1,0.2,0.3], 0.01, 0.03)]

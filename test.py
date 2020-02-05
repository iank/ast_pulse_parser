import pulse
import unittest
import numpy as np

VARS = {
    'Amplitude': 'Amplitude',
    'Pulse2_amplitude': 'Pulse2_amplitude',
}
class ParseTest(unittest.TestCase):
    def setUp(self):
        self.parser = pulse.PulseParser(VARS)

    def test_simple_pulse(self):
        text = 'pulse(0.10, 0.500, Amplitude)'
        expected = [(0.10, 0.500, 'Amplitude')]
        got = self.parser.parse(text)
        self.assertEqual(got, expected)

    def test_pulse_some_keyword_args(self):
        text = 'pulse(0.10, 0.500, values=Amplitude)'
        expected = [(0.10, 0.500, 'Amplitude')]
        got = self.parser.parse(text)
        self.assertEqual(got, expected)

    def test_sum_of_pulses_with_units_and_keywords(self):
        text = "pulse(0.01, 0.01, 10*mV) + \npulse(\n  times=0.1 + np.linspace(0, 0.01 * (10-1), 10),\n  widths=0.005,\n  values=20*mV\n) + \npulse(0.25, 0.014, Pulse2_amplitude)"
        expected = [(0.01, 0.01, 0.01), ([0.1 , 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19], 0.005, 0.02), (0.25, 0.014, 'Pulse2_amplitude')]
        got = self.parser.parse(text)
        self.assertEqual(got[0], expected[0])
        self.assertEqual(got[2], expected[2])

        self.assertEqual(got[1][2], expected[1][2])
        self.assertEqual(got[1][1], expected[1][1])
        self.assertTrue(np.allclose(got[1][0], expected[1][0]))

    def test_pulse_with_keywords_order(self):
        text = 'pulse(widths=0.01, times=[0.1,0.2,0.3], values=30*mV)'
        expected = [([0.1,0.2,0.3], 0.01, 0.03)]
        got = self.parser.parse(text)
        self.assertEqual(got, expected)

    def test_pulse_with_addVar(self):
        text = 'pulse(widths=dogs, times=[0.1,0.2,0.3], values=30*cats)'
        expected = [([0.1,0.2,0.3], 'dogs', 300)]
        self.parser.addVar('cats', 10)
        self.parser.addVar('dogs')
        got = self.parser.parse(text)
        self.assertEqual(got, expected)

if __name__ == '__main__':
    unittest.main()

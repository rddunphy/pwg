import unittest

from generator.generator import generate, IllegalPatternException


class GeneratorTest(unittest.TestCase):

    def testBasic(self):
        pattern = "lunNsxSaAhHbcC"
        password = generate(pattern)
        self.assertEqual(len(password), 14)

    def testLengthDescriptor(self):
        pattern = "a{10}"
        password = generate(pattern)
        self.assertEqual(len(password), 10)

    def testRangeDescriptor(self):
        pattern = "h{5-6}"
        password = generate(pattern)
        self.assertGreaterEqual(len(password), 5)
        self.assertLessEqual(len(password), 6)

    def testOptionalDescriptor(self):
        pattern = "nN?"
        password = generate(pattern)
        self.assertGreaterEqual(len(password), 1)
        self.assertLessEqual(len(password), 2)

    def testOrdered(self):
        pattern = "onu{20}n"
        password = generate(pattern)
        self.assertEqual(len(password), 22)
        try:
            int(password[0])
            int(password[21])
        except ValueError:
            self.fail("Numerals not at expected indices")

    def testIllegalCharacterClass(self):
        pattern = "nay"
        with self.assertRaises(IllegalPatternException):
            generate(pattern)

    def testIllegalOrderedPlacement(self):
        pattern = "no"
        with self.assertRaises(IllegalPatternException):
            generate(pattern)

    def testIllegalDescriptorRange(self):
        pattern = "n{20-10}"
        with self.assertRaises(IllegalPatternException):
            generate(pattern)

    def testDescriptorRangeSyntaxError(self):
        pattern = "n{10-20"
        with self.assertRaises(IllegalPatternException):
            generate(pattern)

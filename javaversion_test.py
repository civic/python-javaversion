from parser import ParserError
import unittest
from javaversion import JavaVersion


class JavaVersionTest(unittest.TestCase):
    def test_isValidがTrue(self):
        self.assertTrue(JavaVersion.isValid("JDK7u40"))
        self.assertTrue(JavaVersion.isValid("JDK1u01"))
    def test_isValidがFalse(self):
        self.assertFalse(JavaVersion.isValid("hoge"))
        self.assertFalse(JavaVersion.isValid("JDK7u9x"))
        self.assertFalse(JavaVersion.isValid("aJDK7u9"))
        self.assertFalse(JavaVersion.isValid("JDK07u9"), "0始まりのFamilyNumberは不可")

    def test_parseしてFamilyNumberとUpdateNumberを取得できる(self):
        v = JavaVersion.parse("JDK7u40")
        self.assertEquals(v.familyNumber, 7)
        self.assertEquals(v.updateNumber, 40)

        v = JavaVersion.parse("JDK7u040")
        self.assertEquals(v.familyNumber, 7)
        self.assertEquals(v.updateNumber, 40)

    def test_parseして例外発生(self):
        self.assertRaises(ParserError, JavaVersion.parse, "JDK7u40x")
        self.assertRaises(ParserError, JavaVersion.parse, "JDK07u4")



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromName("javaversion_test")
    unittest.TextTestRunner(verbosity=2).run(suite)

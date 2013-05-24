from parser import ParserError
import unittest
from javaversion import JavaVersion


class JavaVersionTest(unittest.TestCase):

    def test_isValidがTrue(self):
        self.assertTrue(JavaVersion.isValid("JDK7u40"))
        self.assertTrue(JavaVersion.isValid("JDK1u01"))

    def test_isValidがFalse(self):
        self.assertFalse(JavaVersion.isValid("hoge"))
        self.assertFalse(JavaVersion.isValid("JDK7u9x"), "updateNumberに数字以外")
        self.assertFalse(JavaVersion.isValid("aJDK7u9"), "JDKで始まらない")
        self.assertFalse(JavaVersion.isValid("JDK07u9"), "0始まりのFamilyNumberは不可")

    def test_parseしてFamilyNumberとUpdateNumberを取得できる(self):
        v = JavaVersion.parse("JDK7u40")
        self.assertEquals(v.familyNumber, 7)
        self.assertEquals(v.updateNumber, 40)

        v = JavaVersion.parse("JDK7u040")
        self.assertEquals(v.familyNumber, 7)
        self.assertEquals(v.updateNumber, 40)

    def test_Parseした結果得られるオブジェクトは変更できない(self):
        v = JavaVersion.parse("JDK7u040")
        def 値をセットはできない():
            v.familyNumber = 10

        self.assertRaises(AttributeError, 値をセットはできない)


    def test_parseして例外発生(self):
        self.assertRaises(ParserError, JavaVersion.parse, "JDK7u40x")
        self.assertRaises(ParserError, JavaVersion.parse, "JDK07u4")

    def test_familyNumber40が51より小さい(self):
        u40 = JavaVersion.parse("JDK7u40")
        u51 = JavaVersion.parse("JDK7u51")
        self.assertTrue(u40 < u51)
        self.assertFalse(u51 < u40)

    def test_familyNumber51が40より大きい(self):
        u40 = JavaVersion.parse("JDK7u40")
        u51 = JavaVersion.parse("JDK7u51")

        self.assertTrue(u51 > u40)
        self.assertFalse(u40 > u51)

    def test_updateNumber8が7より大きい(self):
        jdk8 = JavaVersion.parse("JDK8u0")
        u51 = JavaVersion.parse("JDK7u51")
        self.assertTrue(jdk8 > u51)

    def test_updateNumber7が8より小さい(self):
        jdk8 = JavaVersion.parse("JDK8u0")
        u51 = JavaVersion.parse("JDK7u51")
        self.assertTrue(u51 < jdk8)

    def test_同一バージョンはltもgtもfalse(self):
        u51 = JavaVersion.parse("JDK7u51")
        self.assertFalse(u51 < u51)
        self.assertFalse(u51 > u51)
        self.assertTrue(u51 == u51)



if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromName("javaversion_test")
    unittest.TextTestRunner(verbosity=2).run(suite)

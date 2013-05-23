from parser import ParserError
import re


class JavaVersion(object):
    @staticmethod
    def isValid(version_str):
        try:
            JavaVersion.parse(version_str)
            return True
        except ParserError as e:
            return False


    @staticmethod
    def parse(version_str):
        m = re.match(r"""
                ^JDK                # 先頭JDK
                ([1-9][0-9]*)       # familyNumber1桁目は0位外の数字で始まりn桁の数字
                u                   # 固定文字 u
                ([0-9]+)$           # 1桁以上の数字(0可)
                """
            , version_str, re.VERBOSE)
        if m is None:
            raise ParserError("invalid version string.")

        familyNumber = int(m.group(1))
        updateNumber = int(m.group(2))
        return JavaVersion(familyNumber, updateNumber)

    def __init__(self, familyNumber, updateNumber):
        self.familyNumber = familyNumber
        self.updateNumber = updateNumber


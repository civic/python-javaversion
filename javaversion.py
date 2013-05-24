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
        self._familyNumber = familyNumber
        self._updateNumber = updateNumber

    @property
    def familyNumber(self):
        return self._familyNumber

    @property
    def updateNumber(self):
        return self._updateNumber

    def __eq__(self, other):
        return (self.familyNumber == other.familyNumber and
                self.updateNumber == other.updateNumber)

    def __lt__(self, other):
        if self.familyNumber == other.familyNumber:
            return self.updateNumber < other.updateNumber
        return self.familyNumber < other.familyNumber


    def nextLimitedUpdate(self):
        nextUpdateNumber = self.updateNumber + 20 - (self.updateNumber % 20)
        return JavaVersion(self.familyNumber, nextUpdateNumber)

    def nextCriticalPatchUpdate(self):
        nextUpdateNumber = self.updateNumber + 5 - (self.updateNumber % 5)
        if nextUpdateNumber % 2 == 0:
            nextUpdateNumber += 1
        return JavaVersion(self.familyNumber, nextUpdateNumber)

    def nextSecurityAlert(self):
        nextUpdateNumber = self.updateNumber + 1
        if nextUpdateNumber % 5 == 0:
            nextUpdateNumber += 1
        return JavaVersion(self.familyNumber, nextUpdateNumber)

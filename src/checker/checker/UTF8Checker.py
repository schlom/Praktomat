# -*- coding: utf-8 -*-

"""
UTF-8 Checker.
"""
import os
from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import escape
from checker.basemodels import Checker
import codecs
import re

class UTF8Checker(Checker):
    """ Checks if the specified text is encoded as UTF-8 in a submitted file """

    def findInvalidChar(self, data):
        result = False
        log = ""
        regex = r"[^!-~\r\n\t\0\s]"
        matches = re.finditer(regex, data, re.MULTILINE)
        for matchNum, match in enumerate(matches):
            matchNum = matchNum + 1
            log += match.group() + " "
            result = True
        return log, result

    def _getLines(self, text):
        """ Returns a list of lines (as strings) from text """
        lines = text.split("\n")
        return lines

    def isBOM(self, data):
        if data.startswith(codecs.BOM_UTF8):
            return True
        else:
            return False

    def isUTF8(self, data):
        try:
            f = codecs.open(data, encoding='utf-8', errors='strict')
            for line in f:
                pass
            return True
        except UnicodeDecodeError:
            return False

    def title(self):
        """Returns the title for this checker category."""
        return "UTF-8 Checker"

    @staticmethod
    def description():
        """ Returns a description for this Checker. """
        return u"This test is passed if all files are encoded in UTF-8 and do not contain invalid characters"

    def run(self, env):
        """ Checks if the specified text is included in a submitted file """
        result = self.create_result(env)
        
        passed = 1
        log = ""
        lines = []
        
        # search the sources
        for (name, content) in env.sources():
            further_checks = 1
            # Look at the raw data
            filepath = os.path.join(env.tmpdir(),os.path.basename(name))
            with open(filepath, mode='rb') as f:
                raw_bytes = f.read()
            if self.isBOM(raw_bytes):
                log += "<strong>" + escape(name) + "</strong> contains Byte Order Mark, which is not allowed!<br>"
                passed = 0
                further_checks = 0
            if not self.isUTF8(filepath):
                log += "<strong>" + escape(name) + "</strong> is not a UTF-8 file!<br>"
                passed = 0
                further_checks = 0
            if further_checks == 1:
                lines = self._getLines(content)
                lineNum = 1
                do_once = 1
                for line in lines:                    
                    txt, invalid = self.findInvalidChar(line)
                    if invalid:
                        passed = 0
                        if do_once == 1:
                            log += "<strong>" + escape(name) + "</strong> has invalid character(s) in<br>"
                            do_once = 0
                        log += "&nbsp&nbsp&nbsp&nbsp line " + str(lineNum) + ": &nbsp&nbsp" + txt + "<br>"
                    lineNum += 1
        
        result.set_log(log)
        result.set_passed(passed)
        return result

from checker.admin import CheckerInline


class UTF8CheckerInline(CheckerInline):
    model = UTF8Checker

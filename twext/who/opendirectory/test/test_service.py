##
# Copyright (c) 2013 Apple Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##

"""
OpenDirectory service tests.
"""

from twisted.trial import unittest
from twext.who.opendirectory import DirectoryService
from twext.who.expression import (
    CompoundExpression, MatchExpression, MatchType, Operand
)





class OpenDirectoryServiceTestCase(unittest.TestCase):
    """
    Tests for L{DirectoryService}.
    """

    def test_queryStringFromExpression(self):
        service = DirectoryService()
        expression = MatchExpression(
            service.fieldName.shortNames, u"xyzzy",
            matchType=MatchType.equals
        )
        query = service._queryStringFromExpression(expression)
        self.assertEquals(query, u"(dsAttrTypeStandard:RecordName=xyzzy)")

        expression = CompoundExpression(
            [
                MatchExpression(
                    service.fieldName.shortNames, u"xyzzy",
                    matchType=MatchType.contains
                ),
                MatchExpression(
                    service.fieldName.emailAddresses, u"plugh",
                    matchType=MatchType.startsWith
                ),
                MatchExpression(
                    service.fieldName.fullNames, u"foo",
                    matchType=MatchType.equals
                ),
            ],
            Operand.AND
        ) 
        query = service._queryStringFromExpression(expression)
        self.assertEquals(query,
            u"(&(dsAttrTypeStandard:RecordName=*xyzzy*)"
             "(dsAttrTypeStandard:EMailAddress=plugh*)"
             "(dsAttrTypeStandard:RealName=foo))"
        )

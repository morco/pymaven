#
# Copyright (c) 2015 SAS Institute, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest

from libmaven import Artifact
from libmaven import VersionRange
from libmaven.errors import ArtifactParseError


class TestArtifact(unittest.TestCase):
    def _assertArtifactOrder(self, a1, a2):
        assert a1 < a2
        assert a2 > a1
        assert not a1 >= a2
        assert not a2 <= a1
        assert not a1 == a2
        assert a1 != a2

    def test_fromstring(self):
        v1 = VersionRange.fromstring("1")
        test_pairs = (
            ("foo:bar:1", ("foo", "bar", v1, "jar", None)),
            ("foo:bar:pkg:1", ("foo", "bar", v1, "pkg", None)),
            ("foo:bar:pkg:sources:1", ("foo", "bar", v1, "pkg", "sources")),
            ("foo:bar:pkg:javadoc:1", ("foo", "bar", v1, "pkg", "javadoc")),
            )

        for input, expected in test_pairs:
            artifact = Artifact.fromstring(input)
            assert artifact.coordinate == expected

    def test_invalid_coordinates(self):
        tests = ("foo:bar", "foo")
        for input in tests:
            self.assertRaises(ArtifactParseError, Artifact.fromstring, input)

    def test_path(self):
        v1 = VersionRange.fromstring("1")
        test_pairs = (
            ("foo:bar:1", "/foo/bar/1/bar-1.jar"),
            ("foo:bar:pkg:1", "/foo/bar/1/bar-1.pkg"),
            ("foo:bar:pkg:sources:1", "/foo/bar/1/bar-1-sources.pkg"),
            ("foo:bar:pkg:javadoc:1", "/foo/bar/1/bar-1-javadoc.pkg"),
            )

        for input, expected in test_pairs:
            artifact = Artifact.fromstring(input)
            assert artifact.path == expected

    def test_comparison(self):
        test_pairs = (
            # compare group id
            (Artifact("f", "a", "1"), Artifact("g", "a", "1")),
            # compare artifact id
            (Artifact("g", "a", "1"), Artifact("g", "b", "1")),
            # compare type
            (Artifact("g", "a", "1"), Artifact("g", "a", "1", "pom")),
            (Artifact("g", "a", "1", "jar"), Artifact("g", "a", "1", "pom")),
            (Artifact("g", "a", "1", "pom"), Artifact("g", "a", "1", "war")),
            # compare classifier
            (Artifact("g", "a", "1", classifier="c"), Artifact("g", "a", "1")),
            (Artifact("g", "a", "1", classifier="a"), Artifact("g", "a", "1", classifier="c")),
            # compare version
            (Artifact("g", "a", "1"), Artifact("g", "a", "2")),
            # mask version
            (Artifact("f", "a", "2"), Artifact("g", "a", "1")),
            (Artifact("g", "a", "2"), Artifact("g", "b", "1")),
            (Artifact("g", "a", "2"), Artifact("g", "a", "1", "pom")),
            (Artifact("g", "a", "2", "jar"), Artifact("g", "a", "1", "pom")),
            (Artifact("g", "a", "2", "pom"), Artifact("g", "a", "1", "war")),
            (Artifact("g", "a", "2", classifier="c"), Artifact("g", "a", "1")),
            (Artifact("g", "a", "2", classifier="a"), Artifact("g", "a", "1", classifier="c")),
            )

        for pair in test_pairs:
            self._assertArtifactOrder(*pair)

        # verify identity
        a = Artifact("foo", "bar", "1")
        assert not a < a
        assert a <= a
        assert a >= a
        assert a == a
        assert not a != a

        # compare to non-artifact
        assert a > "aardvark"
        assert a != "aardvark"
        assert a > 10

    def test_tostring(self):
        a = Artifact("foo", "bar", "1")
        assert str(a) == "foo:bar:jar:1"

        a = Artifact("foo", "bar", "1", "pom")
        assert str(a) == "foo:bar:pom:1"

        a = Artifact("foo", "bar", "1", "pom", classifier="sources")
        assert str(a) == "foo:bar:pom:sources:1"

        a = Artifact("foo", "bar", "1", "pom", classifier="sources",
                     scope="compile")
        assert str(a) == "foo:bar:pom:sources:1:compile"
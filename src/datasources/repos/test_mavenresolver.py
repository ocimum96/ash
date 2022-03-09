import imp
from unittest import TestCase, main
from datasources.repos.mavenresolver import MavenResolver

class TestMavenResolver(TestCase):
    def test_get_metadata(self):
        resolver = MavenResolver("abbot", "costello", None )
        resolver.ResolveMetadata()

if __name__ == '__main__':
    main()
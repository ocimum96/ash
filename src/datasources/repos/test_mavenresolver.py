from curses import meta
from unittest import TestCase, main
from datasources.repos.mavenresolver import MavenResolver

class TestMavenResolver(TestCase):
	def test_get_metadata(self):
		resolver = MavenResolver("abbot", "costello", None )
		data = resolver.ResolveMetadata()
		assert data is not None # Data must resolve
	
	def test_get_pom(self):
		r = MavenResolver("atlassian-core", "atlassian-core", "2.5.2")
		data = r.ResolvePOMfile()
		assert data is not None # Data must resolve
	
	def test_get_metadata_and_pom(self):
		r = MavenResolver("atlassian-core", "atlassian-core", "2.5.2")
		metadata = r.ResolveMetadata()
		assert metadata is not None # Data must resolve
		pom =  r.ResolvePOMfile()
		assert pom is not None # Data must resolve
	
	def test_get_metadata_and_pom_404(self):
		r = MavenResolver("dummy", "does-not-exists", "1.0.0-SNAPSHOT")
		with self.assertRaises(MavenResolver.FileNotResolvedException):
			metadata = r.ResolveMetadata()
			assert metadata is None # Data shall be none, exception occured.
		with self.assertRaises(MavenResolver.FileNotResolvedException):
			pom =  r.ResolvePOMfile()
			assert pom is None # Data shall be none, exception occured.

if __name__ == '__main__':
	main()
import unittest
from unittest.mock import Mock
from pyproj import CRS
from catdel import Projection  # replace 'your_module' with the actual module name

# Mock configuration class for testing
class MockConfig:
    dst_crs = "EPSG:4326"
    geographic_crs = "EPSG:3857"

class TestProjection(unittest.TestCase):
    
    def setUp(self):
        self.config = MockConfig()
        self.projection = Projection(self.config)

    def test_folium_proj(self):
        self.assertEqual(self.projection.folium_proj, "EPSG4326")

    def test_pyproj(self):
        proj = self.projection.pyproj
        self.assertIsInstance(proj, CRS)
        self.assertEqual(proj.srs, "EPSG:4326")

    def test_transform_to_geo(self):
        x, y = 500000, 5000000
        lat, lon = self.projection.to_geo(x, y)
        self.assertIsInstance(lat, float)
        self.assertIsInstance(lon, float)

    def test_transform_from_geo(self):
        lat, lon = 45.0, 45.0
        x, y = self.projection.from_geo(lat, lon)
        self.assertIsInstance(x, float)
        self.assertIsInstance(y, float)

    def test_transform_array_to_geo(self):
        coordinates = [(500000, 5000000), (600000, 6000000)]
        transformed_coords = self.projection.transform_array_to_geo(coordinates)
        self.assertEqual(len(transformed_coords), len(coordinates))
        for lat, lon in transformed_coords:
            self.assertIsInstance(lat, float)
            self.assertIsInstance(lon, float)

if __name__ == '__main__':
    unittest.main()

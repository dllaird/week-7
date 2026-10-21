import unittest
from loader import *

class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        # known values from Google Maps
        expected = [
            ("Museum of Modern Art", 40.7618552, -73.9782438, "Museum"),
            ("USS Alabama Battleship Memorial Park", 30.684373, -88.015316,
             "Park"),
        ]

        geolocator = get_geolocator()
        df = build_geo_dataframe(geolocator, [row[0] for row in expected])

        # one row per location
        self.assertEqual(len(df), len(expected))

        for i, (loc, lat, lon, loc_type) in enumerate(expected):
            row = df.iloc[i]

            # subTest reports each location separately if one fails
            with self.subTest(location=loc):
                self.assertEqual(row["location"], loc)

                # Nominatim and Google Maps differ slightly so allow tolerance
                self.assertAlmostEqual(row["latitude"], lat, delta=0.01)
                self.assertAlmostEqual(row["longitude"], lon, delta=0.01)

                self.assertEqual(row["type"], loc_type)

    def test_invalid_location(self):
        geolocator = get_geolocator()
        df = build_geo_dataframe(geolocator, ["asdfqwer1234"])

        # the row should still exist and keep the location name
        self.assertEqual(len(df), 1)
        row = df.iloc[0]
        self.assertEqual(row["location"], "asdfqwer1234")

        # everything else should be NA
        for col in ["latitude", "longitude", "type"]:
            with self.subTest(column=col):
                self.assertTrue(pd.isna(row[col]),
                                f"{col} should be NA for a nonexistent location.")

if __name__ == "__main__":
    unittest.main()

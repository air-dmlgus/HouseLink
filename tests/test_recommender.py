"""Run with: python -m unittest discover -s tests -v"""
import unittest

from recommender import FEATURES, PROFILES, cluster_areas, load_areas, recommend


class RecommenderTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.areas = load_areas()

    def test_sample_data_is_valid(self):
        self.assertGreaterEqual(len(self.areas), 3)
        for area in self.areas:
            self.assertTrue(all(0 <= area[key] <= 100 for key in FEATURES))

    def test_ranking_is_descending(self):
        for profile in PROFILES:
            results = recommend(self.areas, profile)
            self.assertEqual(len(results), len(self.areas))
            self.assertEqual(
                [row["score"] for row in results],
                sorted((row["score"] for row in results), reverse=True),
            )

    def test_profiles_change_top_recommendation(self):
        safety_top = recommend(self.areas, "safety")[0]["district"]
        education_top = recommend(self.areas, "education")[0]["district"]
        self.assertNotEqual(safety_top, education_top)

    def test_invalid_profile_is_rejected(self):
        with self.assertRaises(ValueError):
            recommend(self.areas, "unknown")

    def test_clusters_are_deterministic(self):
        first = cluster_areas(self.areas, k=3)
        self.assertEqual(first, cluster_areas(self.areas, k=3))
        self.assertEqual(len(first), len(self.areas))
        self.assertTrue(all(0 <= label < 3 for label in first))


if __name__ == "__main__":
    unittest.main()

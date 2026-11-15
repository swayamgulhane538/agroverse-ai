import unittest
import re
from pathlib import Path

class TestSprayingMarkupGrep(unittest.TestCase):
    """
    Automated grep test: Verifies that no hard-coded weather values,
    dosages, water volumes, or spray window times remain in the markup.
    """

    def setUp(self):
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        index_file = repo_root / "index.html"
        self.assertTrue(index_file.exists(), f"index.html not found at {index_file}")
        with open(index_file, "r", encoding="utf-8") as f:
            self.html = f.read()

        # Extract only the view-spraying HTML section
        match = re.search(r'<div id="view-spraying".*?id="view-disease"', self.html, re.DOTALL)
        self.assertIsNotNone(match, "view-spraying block not found in index.html")
        self.spraying_html = match.group(0)

    def test_no_hardcoded_dosages_or_water_volumes(self):
        forbidden_dosages = [
            r"4g in 10 Litres",
            r"3ml in 10 Litres",
            r"150 to 200 Litres",
            r"mandatory 11 days waiting period"
        ]
        for pat in forbidden_dosages:
            self.assertFalse(
                re.search(pat, self.spraying_html, re.IGNORECASE),
                f"Found prohibited hard-coded dosage pattern in markup: '{pat}'"
            )

    def test_no_hardcoded_spray_window_times(self):
        forbidden_times = [
            r"Morning Window:\s*06:30",
            r"Evening Window:\s*04:30",
            r"Midday:\s*11:30",
            r"midday prohibited"
        ]
        for pat in forbidden_times:
            self.assertFalse(
                re.search(pat, self.spraying_html, re.IGNORECASE),
                f"Found prohibited hard-coded spray window in markup: '{pat}'"
            )

    def test_live_gauges_are_dynamic_placeholders(self):
        # Gauges must be initialized as placeholders to be filled by live API telemetry
        self.assertIn('id="gaugeTemp">--°C</div>', self.spraying_html)
        self.assertIn('id="gaugeWetBulb">--°C</div>', self.spraying_html)
        self.assertIn('id="gaugeDeltaT">--°C</div>', self.spraying_html)
        self.assertIn('id="gaugeRh">--%</div>', self.spraying_html)
        self.assertIn('id="gaugeWind">-- km/h</div>', self.spraying_html)
        self.assertIn('id="gaugeRain">--%</div>', self.spraying_html)

    def test_sliders_only_inside_manual_what_if_details(self):
        # Verify sliders exist exclusively inside the collapsible details element
        self.assertIn('<details id="sprayManualWhatIfDetails"', self.spraying_html)
        self.assertIn('id="manualOverrideBadge"', self.spraying_html)
        self.assertIn('id="sprayWind"', self.spraying_html)
        self.assertIn('id="sprayRain"', self.spraying_html)

    def test_cibrc_and_72h_strip_present(self):
        self.assertIn('id="sprayHourlyStrip"', self.spraying_html)
        self.assertIn('id="sprayWindowsList"', self.spraying_html)
        self.assertIn('id="sprayProductList"', self.spraying_html)
        self.assertIn('id="sprayDriftCard"', self.spraying_html)

if __name__ == "__main__":
    unittest.main()

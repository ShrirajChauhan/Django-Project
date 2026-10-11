from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import json

from django.test import SimpleTestCase

from .views import ISSUES_DATA_FILE, REPORTERS_DATA_FILE, JSONFileAPIView


class EntityDetailAPITests(SimpleTestCase):
    @patch("issues.views._get_record")
    def test_get_issue_by_id(self, get_record):
        get_record.return_value = {"id": 7, "title": "Example issue"}

        response = self.client.get("/issues/7/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 7, "title": "Example issue"})
        get_record.assert_called_once_with(ISSUES_DATA_FILE, 7)

    @patch("issues.views._get_record")
    def test_get_reporter_by_id(self, get_record):
        get_record.return_value = {"id": 12, "name": "Example reporter"}

        response = self.client.get("/reporters/12/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"id": 12, "name": "Example reporter"})
        get_record.assert_called_once_with(REPORTERS_DATA_FILE, 12)

    @patch("issues.views._get_record", return_value=None)
    def test_missing_issue_returns_404(self, get_record):
        response = self.client.get("/issues/404/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Issue not found."})

    @patch("issues.views._get_record", return_value=None)
    def test_missing_reporter_returns_404(self, get_record):
        response = self.client.get("/reporters/404/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Reporter not found."})

    def test_save_record_appends_to_existing_json_records(self):
        with TemporaryDirectory() as temp_dir:
            data_file = Path(temp_dir) / "records.json"
            data_file.write_text('[{"id": 1}]', encoding="utf-8")

            JSONFileAPIView()._save_record(data_file, {"id": 2, "name": "New record"})

            self.assertEqual(
                json.loads(data_file.read_text(encoding="utf-8")),
                [{"id": 1}, {"id": 2, "name": "New record"}],
            )

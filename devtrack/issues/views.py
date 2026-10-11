import json
from pathlib import Path

from rest_framework import status
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.views import APIView

ISSUES_DATA_FILE = Path(__file__).resolve().parent / "files" / "issues.json"
REPORTERS_DATA_FILE = Path(__file__).resolve().parent / "files" / "reporter.json"


def _get_record(data_file: Path, record_id: int) -> dict | None:
    contents = data_file.read_text(encoding="utf-8")
    records = json.loads(contents) if contents.strip() else []

    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise ValueError(f"Expected a JSON list of records in {data_file}")

    return next((record for record in records if record.get("id") == record_id), None)



def _save_record(data_file: Path, record: dict) -> None:
    contents = data_file.read_text(encoding="utf-8")
    records = json.loads(contents) if contents.strip() else []

    if not isinstance(records, list) or any(not isinstance(item, dict) for item in records):
        raise ValueError(f"Expected a JSON list of records in {data_file}")

    records.append(record)
    data_file.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")


class IssueView(APIView):
    def get(self, request, format=None):
        user_id = request.GET.get('id')
        status = request.GET.get('status')
        if user_id:
            issue = _get_record(ISSUES_DATA_FILE, int(user_id))
        elif status:
            # Return issues with the specified status
            contents = ISSUES_DATA_FILE.read_text(encoding="utf-8")
            issues = json.loads(contents) if contents.strip() else []
            issue = [i for i in issues if i.get("status") == status]
        else:
            # Return all issues if no ID is specified
            contents = ISSUES_DATA_FILE.read_text(encoding="utf-8")
            issue = json.loads(contents) if contents.strip() else []
        if issue is None:
            return Response(
                {"error": "Issue not found."},
                status=HTTP_404_NOT_FOUND,
            )
        return Response(issue)

    def post(self, request, format=None):
        new_issue = request.data.copy()
        new_issue["id"] = new_issue.get("id")
        _save_record(ISSUES_DATA_FILE, new_issue)
        return Response(new_issue, status=HTTP_201_CREATED)


class ReporterView(APIView):
    def get(self, request, format=None):
        reporter_id = request.GET.get('id')
        if reporter_id:
            reporter = _get_record(REPORTERS_DATA_FILE, int(reporter_id))
        else:
            # Return all reporters if no ID is specified
            contents = REPORTERS_DATA_FILE.read_text(encoding="utf-8")
            reporter = json.loads(contents) if contents.strip() else []
        if reporter is None:
            return Response(
                {"error": "Reporter not found."},
                status=HTTP_404_NOT_FOUND,
            )
        return Response(reporter)

    def post(self, request, format=None):
        new_reporter = request.data.copy()
        new_reporter["id"] = new_reporter.get("id")
        _save_record(REPORTERS_DATA_FILE, new_reporter)
        return Response(new_reporter, status=HTTP_201_CREATED)
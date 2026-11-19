from unittest.mock import patch

from dds_cli.data_lister import DataLister


def test_list_projects_preserves_missing_updated_dates_and_sorts_them_last():
    lister = DataLister.__new__(DataLister)
    lister.show_usage = False
    lister.token = {}
    lister.json = True
    response = {
        "project_info": [
            {"Project ID": "missing", "Last updated": None},
            {"Project ID": "older", "Last updated": "Thu, 01 Jan 2026 00:00:00 GMT"},
            {"Project ID": "newer", "Last updated": "Fri, 02 Jan 2026 00:00:00 GMT"},
        ]
    }

    with patch(
        "dds_cli.data_lister.dds_cli.utils.perform_request",
        return_value=(response, None),
    ):
        projects = lister.list_projects()

    assert {project["Project ID"] for project in projects[:2]} == {"newer", "older"}
    assert projects[-1]["Project ID"] == "missing"
    assert projects[-1]["Last updated"] is None

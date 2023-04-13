from pathlib import Path

from api.utils import get_project_absolute_path


def test_get_project_absolute_path():
    assert get_project_absolute_path() == Path(__file__).parent.parent.resolve()

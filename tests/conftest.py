import pytest

import sys
from pathlib import Path


# Ensure backend package is importable when running from project root
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture(scope="session")
def app():
    from backend.server import app as flask_app, load_data
    from backend.vector_search import build_index

    # Load data and build index once per test session
    load_data()
    from backend.server import DATA  # re-import to get populated data
    build_index(DATA.get("nonprofits", []))

    yield flask_app


@pytest.fixture()
def client(app):
    return app.test_client()



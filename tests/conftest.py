import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, drop_database
from api.db import Base
from sqlalchemy import create_engine

from api.dependencies.database import get_db
from api.main import app

from api.helpers.load_data import load_data_from_file

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def override_get_db():
    """ " Override"""
    try:
        db = Session(autocommit=False, autoflush=False, bind=engine)
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def create_db():
    """creating db model in database"""

    create_database(SQLALCHEMY_DATABASE_URL)
    print("\n" + "\x1b[6;30;42m" + "Creating test database." + "\x1b[0m")
    # os.environ["api_prefix"] = ""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    db = Session(autocommit=False, autoflush=False, bind=engine)
    # load in test data
    working_directory = os.getcwd()
    # if running tests from inside pycharm
    if "tests" in working_directory:
        load_data_from_file("../tests/testData.json", db)
    else:
        load_data_from_file(working_directory + "/tests/testData.json", db)
    # load_data_from_file(working_directory + "/tests/testData.json", db)
    db.close()

    yield 1

    drop_database(SQLALCHEMY_DATABASE_URL)
    print("\n" + "\x1b[6;30;42m" + "Delete test database." + "\x1b[0m")


@pytest.fixture()
def get_db_session():
    """Getting session for db transaction"""
    session = Session(autocommit=False, autoflush=False, bind=engine)
    yield session

    session.close()


@pytest.fixture()
def client():
    """Getting testclient of app"""
    with TestClient(app) as client:
        yield client

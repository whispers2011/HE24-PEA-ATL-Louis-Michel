import pytest
from sqlalchemy import inspect
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import app.database as database
from app.database import get_session, init_db


@pytest.fixture(name="memory_engine")
def memory_engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    yield engine
    engine.dispose()


def test_get_session_yields_a_session(monkeypatch, memory_engine):
    monkeypatch.setattr(database, "engine", memory_engine)

    sessions = list(get_session())

    assert len(sessions) == 1
    assert isinstance(sessions[0], Session)


def test_init_db_creates_all_metadata_tables(monkeypatch, memory_engine):
    monkeypatch.setattr(database, "engine", memory_engine)

    init_db()

    created = set(inspect(memory_engine).get_table_names())
    assert created == set(SQLModel.metadata.tables.keys())

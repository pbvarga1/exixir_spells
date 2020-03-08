import os
import time

import pytest
import docker

from spells_db.session_context import session_context
from spells_db.models import Base


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture(scope='session')
def docker_container():
    client = docker.from_env()
    # Check if image exists, build if it does not
    image, gen = client.images.build(
        path=TEST_DIR,
        tag='app-test',
        rm=True,
    )
    container = client.containers.run(
        image='app-test',
        ports={'5432/tcp': '5434'},
        detach=True,
        publish_all_ports=True,
    )
    try:
        # wait for postgres to be ready:
        n = 0
        for n, text in enumerate(container.logs(stream=True)):
            if b'database system is ready to accept connections' in text:
                time.sleep(2)
                break
            elif n < 100:
                continue

        # Postgres database ready to go
        yield container
    except Exception:
        raise
    finally:
        container.kill()
        container.remove()
        client.images.remove('app-test', force=True)


@pytest.fixture
def session(docker_container, monkeypatch):
    env = {
        'POSTGRES_USER': 'testing',
        'POSTGRES_PASSWORD': 'testpass',
        'POSTGRES_PORT': '5434',
        'POSTGRES_HOST': os.environ.get('DOCKER_IP', '192.168.99.100'),
    }
    for key, var in env.items():
        monkeypatch.setenv(key, var)
    monkeypatch.delenv('SPELLS_ELIXIR', raising=False)
    with session_context() as session:
        engine = session.get_bind()
        metadata = Base.metadata
        metadata.bind = engine
        metadata.drop_all()
        metadata.create_all()
    try:
        yield session
    finally:
        metadata.drop_all(bind=engine)

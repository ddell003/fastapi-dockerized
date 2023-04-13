from api.config import Config

db_name = "test"
db_username = "user"
db_password = "password"
db_host = "xyz.domain.com"
db_port = 123

test_config = {
    "db_name": db_name,
    "db_username": db_username,
    "db_password": db_password,
    "db_host": db_host,
    "db_port": db_port,
}

# Create a config that we can test
config = Config(**test_config)


def test_db_connectionstring():
    assert isinstance(config.get_db_uri(), str)
    assert (
        config.get_db_uri()
        == f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

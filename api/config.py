from pydantic import BaseSettings


class Config(BaseSettings):
    """
    A global configuration for the service.
    Env Vars will be read as part of the BaseSettings implementation.
    Env Vars of format SOME_VAR will properly be keyed as some_var in the config.
    """

    # The database name
    db_name: str = "api"

    # The username to use to connect to the database
    db_username: str = "api_user"

    # The password to use to connect to the database
    db_password: str = "P4ssW0rd"  # override this

    # The hostname of the database instance
    db_host: str = ""

    # The port of the database instance
    db_port: int = 5432

    # The prefix for all api operations e.g. http(s)://service_domain/{api_prefix}/api/method
    # This value should start with a '/' and not have a trailing '/'
    # ex: /api or /api/v1 and NOT /api/ or /api/v1/
    api_prefix: str = "/api"

    # A whitelist of users for WRITE authorization to certain API endpoints
    # Valid values for this config:
    #   "*" - Allows access regardless of any check
    #   "value1;value2;value3" - A semi-colon delimited string with each value being granted access
    api_authorized_whitelist: str = "*"

    # A domain list for READ authorization to the API endpoints
    # Valid values for this config:
    #   "*" - Allows access regardless of any check
    #   "value1;value2;value3" - A semi-colon delimited string with each value being a domain string like "xyz.com"
    api_authorized_domains: str = "*"

    allowed_origin: str = "http://localhost:3000"

    # Absolute path to where the data lives.
    # We can override the default to load test data instead
    init_data_path: str = ""

    def get_db_uri(self) -> str:
        """
        Gets the database URI connection string from the configured values.
        """
        return f"postgresql://{self.db_username}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Create an instance which can be used throughout the application
config = Config()

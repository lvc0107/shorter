import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from shorter_app.config import FixedConfig


class BuildDatabase:
    def build(self):
        engine = create_engine(
            FixedConfig.ROOT_DATABASE_URI + "/postgres", isolation_level="AUTOCOMMIT"
        )
        self.drop_database_if_exists(engine, FixedConfig.DATABASE_NAME)
        self.create_database(engine, FixedConfig.DATABASE_NAME)
        engine = create_engine(
            FixedConfig.ROOT_DATABASE_URI + "/" + FixedConfig.DATABASE_NAME,
            isolation_level="AUTOCOMMIT",
        )
        self.apply_migration(engine)
        sessionmaker(bind=engine)()

    def create_database(self, engine, database_name):
        engine.execute(f"CREATE DATABASE {database_name}")

    def apply_migration(self, engine, alembic_config_file="alembic.ini"):
        current_directory = os.getcwd()
        root_directory = os.path.split(os.path.realpath(__file__))[0]
        os.chdir(root_directory)
        with engine.begin() as connection:
            alembic_config = Config(alembic_config_file)
            alembic_config.attributes["connection"] = connection
            command.upgrade(alembic_config, "head")
        os.chdir(current_directory)

    def kill_existing_connections(self, engine, database_name):
        query = f"SELECT pg_terminate_backend(pg_stat_activity.pid)\
                FROM pg_stat_activity WHERE pg_stat_activity.datname = '{database_name}' \
                AND pid <> pg_backend_pid();"
        engine.execute(query)

    def drop_database_if_exists(self, engine, database_name):
        query = f"SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('{database_name}')"
        if engine.execute(query).rowcount > 0:
            self.kill_existing_connections(engine, database_name)
            engine.execute(f"DROP DATABASE {database_name}")


if __name__ == "__main__":
    BuildDatabase().build()

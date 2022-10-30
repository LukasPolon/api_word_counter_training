import click

import uvicorn

from app.db.models import word_frequency as word_frequency_models
from .db.base import engine
from .env_config import EnvConfig

env_config = EnvConfig()


@click.group()
def manage():
    """Management CLI for the application."""
    pass


@manage.command("run-app")
def run_app():
    """Application start"""
    # TODO: not the best way to run the application, especially if its not configurable
    uvicorn.run(
        "app.main:app",
        host=env_config.get("SELF_API_HOST"),
        port=int(env_config.get("SELF_API_PORT")),
        log_level=env_config.get("SELF_API_LOG_LEVEL"),
    )


@click.argument("action", type=click.types.Choice(["create", "delete"]))
@manage.command()
def db(action):
    """Create or delete the database."""
    actions = {
        "create": word_frequency_models.Base.metadata.create_all,
        "delete": word_frequency_models.Base.metadata.drop_all,
    }
    click.echo(f"Selected action: {action}")
    actions[action](bind=engine)

    click.echo(f"Database {action}d.")

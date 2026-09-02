from flask import Flask, render_template

from app.common.logger import get_logger
from app.routes.api import api


logger = get_logger(__name__)


def create_app():
    """
    Create and configure the Flask application.
    """

    app = Flask(__name__)

    # Register API routes
    app.register_blueprint(
        api,
        url_prefix="/api"
    )

    # Frontend route
    @app.route("/")
    def index():
        return render_template("index.html")

    logger.info(
        "Flask application created successfully"
    )

    return app


app = create_app()


if __name__ == "__main__":

    logger.info(
        "Starting Medical RAG Flask application"
    )

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
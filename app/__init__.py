import os
from flask import Flask
from dotenv import load_dotenv


def create_app() -> Flask:
    load_dotenv()

    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder='templates',
        static_folder='../static'
    )

    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        raise RuntimeError('Missing required environment variable: SECRET_KEY')
    app.secret_key = secret_key

    # Ensure instance folders exist
    faces_dir = os.getenv('FACES_DIR', os.path.join(app.instance_path, 'faces'))
    os.makedirs(faces_dir, exist_ok=True)

    # Ensure model directory exists when MODEL_PATH is set
    model_path = os.getenv('MODEL_PATH', os.path.join(app.instance_path, 'trained_model.yml'))
    model_dir = os.path.dirname(model_path)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)

    # Register blueprints
    from .routes.main import bp as main_bp
    from .routes.users import bp as users_bp
    from .routes.training import bp as training_bp
    from .routes.recognition import bp as recognition_bp
    from .routes.messaging import bp as messaging_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(training_bp)
    app.register_blueprint(recognition_bp)
    app.register_blueprint(messaging_bp)

    return app



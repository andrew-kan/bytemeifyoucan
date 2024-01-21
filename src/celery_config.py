# celery_config.py
from celery import Celery

def create_celery_app(flask_app=None):
    backend = flask_app.config['CELERY_RESULT_BACKEND'] if flask_app else 'your_default_backend'
    broker = flask_app.config['CELERY_BROKER_URL'] if flask_app else 'your_default_broker'

    celery = Celery(flask_app.import_name if flask_app else 'default', backend=backend, broker=broker)
    
    if flask_app:
        celery.conf.update(flask_app.config)
        # Include context task if Flask app is present
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with flask_app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask

    return celery

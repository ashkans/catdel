import logging
import logging.config

def setup_logging(default_level=logging.INFO):
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': default_level,
            },
        },
        'root': {
            'handlers': ['console'],
            'level': default_level,
        },
    }

    logging.config.dictConfig(logging_config)


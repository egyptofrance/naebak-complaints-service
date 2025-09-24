"""
Manus Evaluator Integration Settings for Naibak Microservices
"""

# Manus Evaluator Configuration
MANUS_EVALUATOR_ENABLED = True
MANUS_EVALUATOR_URL = 'https://8000-i11hedxmx2e1lalatmdgh-08017331.manusvm.computer'

# Manus Control Parameters
MANUS_MAX_TEMPERATURE = 0.1
MANUS_MAX_TOKENS = 5000
MANUS_ENFORCE_HONESTY = True
MANUS_PREVENT_EXAGGERATION = True

# Middleware Configuration
MANUS_MIDDLEWARE = [
    'manus_integration.middleware.ManusEvaluatorMiddleware',
    'manus_integration.middleware.ManusResponseValidatorMiddleware',
]

# Logging Configuration for Manus
MANUS_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'manus_formatter': {
            'format': '[MANUS] {levelname} {asctime} {name} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'manus_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/manus_evaluator.log',
            'formatter': 'manus_formatter',
        },
        'manus_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'manus_formatter',
        },
    },
    'loggers': {
        'manus_integration': {
            'handlers': ['manus_file', 'manus_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Security Settings
MANUS_SECURITY = {
    'REQUIRE_AUTHENTICATION': True,
    'MAX_REQUEST_SIZE': 1024 * 1024,  # 1MB
    'RATE_LIMIT_PER_MINUTE': 60,
    'BLOCKED_PATTERNS': [
        'perfect',
        'flawless', 
        'zero bugs',
        'never fails',
        'guaranteed',
        'absolutely',
        'completely secure',
        'totally safe'
    ]
}

# Integration with existing Django settings
def integrate_manus_settings(django_settings):
    """
    Integrate Manus settings with existing Django settings
    """
    # Add Manus middleware to MIDDLEWARE
    if hasattr(django_settings, 'MIDDLEWARE'):
        django_settings.MIDDLEWARE = list(django_settings.MIDDLEWARE) + MANUS_MIDDLEWARE
    else:
        django_settings.MIDDLEWARE = MANUS_MIDDLEWARE
    
    # Update logging configuration
    if hasattr(django_settings, 'LOGGING'):
        # Merge with existing logging config
        existing_logging = django_settings.LOGGING
        existing_logging['formatters'].update(MANUS_LOGGING['formatters'])
        existing_logging['handlers'].update(MANUS_LOGGING['handlers'])
        existing_logging['loggers'].update(MANUS_LOGGING['loggers'])
    else:
        django_settings.LOGGING = MANUS_LOGGING
    
    # Add Manus-specific settings
    django_settings.MANUS_EVALUATOR_ENABLED = MANUS_EVALUATOR_ENABLED
    django_settings.MANUS_EVALUATOR_URL = MANUS_EVALUATOR_URL
    django_settings.MANUS_MAX_TEMPERATURE = MANUS_MAX_TEMPERATURE
    django_settings.MANUS_MAX_TOKENS = MANUS_MAX_TOKENS
    django_settings.MANUS_ENFORCE_HONESTY = MANUS_ENFORCE_HONESTY
    django_settings.MANUS_PREVENT_EXAGGERATION = MANUS_PREVENT_EXAGGERATION
    django_settings.MANUS_SECURITY = MANUS_SECURITY
    
    return django_settings

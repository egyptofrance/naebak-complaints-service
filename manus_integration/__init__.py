"""
Manus Evaluator Integration Package for Naibak Microservices

This package provides seamless integration between Naibak microservices
and the Manus Evaluator & Compliance Oracle system to prevent exaggeration
and ensure accurate AI responses.
"""

__version__ = "1.0.0"
__author__ = "Manus AI"

from .middleware import ManusEvaluatorMiddleware, ManusResponseValidatorMiddleware
from .settings import integrate_manus_settings

__all__ = [
    'ManusEvaluatorMiddleware',
    'ManusResponseValidatorMiddleware', 
    'integrate_manus_settings'
]

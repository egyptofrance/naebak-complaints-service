"""
Manus Evaluator Client for Naibak Microservices
Provides a simple interface to interact with the Manus Evaluator system
"""

import json
import logging
import requests
from typing import Dict, Any, Optional
from django.conf import settings

logger = logging.getLogger('manus_integration')

class ManusEvaluatorClient:
    """
    Client for interacting with the Manus Evaluator & Compliance Oracle
    """
    
    def __init__(self):
        self.base_url = getattr(
            settings, 
            'MANUS_EVALUATOR_URL', 
            'https://8000-i11hedxmx2e1lalatmdgh-08017331.manusvm.computer'
        )
        self.enabled = getattr(settings, 'MANUS_EVALUATOR_ENABLED', True)
        self.timeout = 30
        
    def evaluate_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Evaluate a Manus AI request before execution
        
        Args:
            prompt: The prompt to be sent to Manus AI
            **kwargs: Additional parameters
            
        Returns:
            Dict containing evaluation results
        """
        if not self.enabled:
            return {'approved': True, 'reason': 'Evaluator disabled'}
            
        try:
            request_data = {
                'prompt': prompt,
                'temperature': kwargs.get('temperature', 0.1),
                'max_tokens': kwargs.get('max_tokens', 5000),
                'enforce_honesty': kwargs.get('enforce_honesty', True),
                'prevent_exaggeration': kwargs.get('prevent_exaggeration', True),
                'service_name': kwargs.get('service_name', 'unknown'),
                'user_id': kwargs.get('user_id', 'anonymous')
            }
            
            response = requests.post(
                f"{self.base_url}/api/evaluate",
                json=request_data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Manus evaluation completed: {result.get('score', 0)}")
                return result
            else:
                logger.warning(f"Manus evaluator returned {response.status_code}")
                return {'approved': True, 'reason': 'Evaluator error, allowing request'}
                
        except requests.RequestException as e:
            logger.error(f"Failed to reach Manus Evaluator: {str(e)}")
            return {'approved': True, 'reason': 'Evaluator unreachable, allowing request'}
        except Exception as e:
            logger.error(f"Manus evaluation error: {str(e)}")
            return {'approved': True, 'reason': 'Evaluation error, allowing request'}
    
    def validate_response(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        Validate a Manus AI response after generation
        
        Args:
            content: The generated content to validate
            **kwargs: Additional parameters
            
        Returns:
            Dict containing validation results
        """
        if not self.enabled:
            return {'valid': True, 'reason': 'Validator disabled'}
            
        try:
            validation_data = {
                'content': content,
                'type': 'response_validation',
                'service_name': kwargs.get('service_name', 'unknown'),
                'user_id': kwargs.get('user_id', 'anonymous')
            }
            
            response = requests.post(
                f"{self.base_url}/api/validate-response",
                json=validation_data,
                timeout=15,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Manus validation completed: {result.get('valid', True)}")
                return result
            else:
                logger.warning(f"Manus validator returned {response.status_code}")
                return {'valid': True, 'reason': 'Validator error, allowing response'}
                
        except requests.RequestException as e:
            logger.error(f"Failed to reach Manus Validator: {str(e)}")
            return {'valid': True, 'reason': 'Validator unreachable, allowing response'}
        except Exception as e:
            logger.error(f"Manus validation error: {str(e)}")
            return {'valid': True, 'reason': 'Validation error, allowing response'}
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Check the health status of the Manus Evaluator system
        
        Returns:
            Dict containing health status
        """
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {'status': 'unhealthy', 'code': response.status_code}
                
        except requests.RequestException as e:
            return {'status': 'unreachable', 'error': str(e)}
    
    def controlled_manus_request(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Make a controlled request to Manus AI with evaluation
        
        Args:
            prompt: The prompt for Manus AI
            **kwargs: Additional parameters
            
        Returns:
            Dict containing the controlled response
        """
        # First, evaluate the request
        evaluation = self.evaluate_request(prompt, **kwargs)
        
        if not evaluation.get('approved', False):
            return {
                'success': False,
                'error': 'Request blocked by Manus Evaluator',
                'reason': evaluation.get('reason', 'Unknown'),
                'details': evaluation
            }
        
        # If approved, make the actual Manus request with controlled parameters
        controlled_params = {
            'temperature': min(kwargs.get('temperature', 0.1), 0.1),
            'max_tokens': min(kwargs.get('max_tokens', 5000), 5000),
            'enforce_honesty': True,
            'prevent_exaggeration': True
        }
        
        # Here you would integrate with your actual Manus AI client
        # For now, return a simulated response
        simulated_response = f"[CONTROLLED MANUS RESPONSE] Based on your request: {prompt[:100]}..."
        
        # Validate the response
        validation = self.validate_response(simulated_response, **kwargs)
        
        if not validation.get('valid', True):
            return {
                'success': False,
                'error': 'Response blocked by Manus Validator',
                'reason': validation.get('reason', 'Unknown'),
                'safe_alternative': validation.get('safe_alternative', 'Content not available')
            }
        
        return {
            'success': True,
            'response': simulated_response,
            'evaluation': evaluation,
            'validation': validation,
            'controlled_params': controlled_params
        }

# Global client instance
manus_client = ManusEvaluatorClient()

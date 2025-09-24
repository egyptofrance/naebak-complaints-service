"""
Manus Evaluator Integration Middleware for Naibak Microservices
This middleware intercepts all Manus AI requests and ensures they pass through
the Manus Evaluator & Compliance Oracle system before execution.
"""

import json
import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class ManusEvaluatorMiddleware(MiddlewareMixin):
    """
    Middleware to intercept and validate all Manus AI requests
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.manus_evaluator_url = getattr(
            settings, 
            'MANUS_EVALUATOR_URL', 
            'https://8000-i11hedxmx2e1lalatmdgh-08017331.manusvm.computer'
        )
        self.enabled = getattr(settings, 'MANUS_EVALUATOR_ENABLED', True)
        super().__init__(get_response)

    def process_request(self, request):
        """
        Process incoming requests and check for Manus AI calls
        """
        if not self.enabled:
            return None
            
        # Check if this is a Manus AI request
        if self._is_manus_request(request):
            return self._validate_manus_request(request)
        
        return None

    def _is_manus_request(self, request):
        """
        Determine if this request involves Manus AI
        """
        # Check URL patterns that indicate Manus usage
        manus_patterns = [
            '/api/generate',
            '/api/ai',
            '/generate',
            '/ai-assist',
            '/manus'
        ]
        
        for pattern in manus_patterns:
            if pattern in request.path:
                return True
                
        # Check request body for Manus-related content
        if hasattr(request, 'body') and request.body:
            try:
                body = json.loads(request.body.decode('utf-8'))
                if any(key in body for key in ['prompt', 'ai_request', 'manus_prompt']):
                    return True
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
                
        return False

    def _validate_manus_request(self, request):
        """
        Send request to Manus Evaluator for validation
        """
        try:
            # Extract request data
            request_data = self._extract_request_data(request)
            
            # Send to Manus Evaluator
            evaluator_response = requests.post(
                f"{self.manus_evaluator_url}/api/evaluate",
                json=request_data,
                timeout=30,
                headers={'Content-Type': 'application/json'}
            )
            
            if evaluator_response.status_code == 200:
                evaluation_result = evaluator_response.json()
                
                # Check if request is approved
                if not evaluation_result.get('approved', False):
                    return JsonResponse({
                        'error': 'Request blocked by Manus Evaluator',
                        'reason': evaluation_result.get('reason', 'Potential exaggeration detected'),
                        'details': evaluation_result.get('details', {}),
                        'blocked': True
                    }, status=400)
                    
                # Log approved request
                logger.info(f"Manus request approved: {evaluation_result.get('score', 0)}")
                
            else:
                # If evaluator is down, log warning but allow request
                logger.warning(f"Manus Evaluator unavailable: {evaluator_response.status_code}")
                
        except requests.RequestException as e:
            # If evaluator is unreachable, log error but allow request
            logger.error(f"Failed to reach Manus Evaluator: {str(e)}")
            
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Manus Evaluator middleware error: {str(e)}")
            
        return None

    def _extract_request_data(self, request):
        """
        Extract relevant data from Django request for evaluation
        """
        data = {
            'method': request.method,
            'path': request.path,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'timestamp': str(request.META.get('HTTP_DATE', '')),
        }
        
        # Extract body data
        if hasattr(request, 'body') and request.body:
            try:
                data['body'] = json.loads(request.body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                data['body'] = request.body.decode('utf-8', errors='ignore')
                
        # Extract query parameters
        if request.GET:
            data['query_params'] = dict(request.GET)
            
        return data

class ManusResponseValidatorMiddleware(MiddlewareMixin):
    """
    Middleware to validate Manus AI responses before sending to client
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.manus_evaluator_url = getattr(
            settings, 
            'MANUS_EVALUATOR_URL', 
            'https://8000-i11hedxmx2e1lalatmdgh-08017331.manusvm.computer'
        )
        self.enabled = getattr(settings, 'MANUS_EVALUATOR_ENABLED', True)
        super().__init__(get_response)

    def process_response(self, request, response):
        """
        Process outgoing responses and validate Manus AI content
        """
        if not self.enabled:
            return response
            
        # Check if response contains Manus AI content
        if self._contains_manus_content(response):
            validated_response = self._validate_manus_response(response)
            if validated_response:
                return validated_response
                
        return response

    def _contains_manus_content(self, response):
        """
        Check if response contains AI-generated content
        """
        if not hasattr(response, 'content'):
            return False
            
        try:
            content = response.content.decode('utf-8')
            # Look for indicators of AI-generated content
            ai_indicators = [
                'generated by',
                'ai response',
                'manus generated',
                'artificial intelligence'
            ]
            
            content_lower = content.lower()
            return any(indicator in content_lower for indicator in ai_indicators)
            
        except UnicodeDecodeError:
            return False

    def _validate_manus_response(self, response):
        """
        Validate Manus AI response content
        """
        try:
            content = response.content.decode('utf-8')
            
            # Send to Manus Evaluator for response validation
            validation_data = {
                'content': content,
                'type': 'response_validation'
            }
            
            evaluator_response = requests.post(
                f"{self.manus_evaluator_url}/api/validate-response",
                json=validation_data,
                timeout=15,
                headers={'Content-Type': 'application/json'}
            )
            
            if evaluator_response.status_code == 200:
                validation_result = evaluator_response.json()
                
                if not validation_result.get('valid', True):
                    # Replace response with safe alternative
                    safe_response = JsonResponse({
                        'error': 'Response blocked by Manus Evaluator',
                        'reason': 'Content validation failed',
                        'safe_alternative': validation_result.get('safe_alternative', 'Content not available'),
                        'blocked': True
                    }, status=200)
                    
                    logger.warning(f"Manus response blocked: {validation_result.get('reason', 'Unknown')}")
                    return safe_response
                    
        except Exception as e:
            logger.error(f"Manus response validation error: {str(e)}")
            
        return None

"""
AI Recommendation Service for problem analysis and solution generation.
"""
import time
from typing import List, Dict
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class AIRecommendationService:
    """Service for generating AI-powered recommendations for user problems."""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.max_response_time = 5  # seconds
        
    def generate_recommendations(self, problem_text: str) -> List[Dict[str, str]]:
        """
        Generate solution recommendations for a given problem.
        
        Args:
            problem_text: The problem description from the user
            
        Returns:
            List of recommendation dictionaries with 'title' and 'description' keys
            
        Raises:
            Exception: If recommendation generation fails
        """
        start_time = time.time()
        
        try:
            if self.api_key:
                # Use OpenAI API for recommendations
                recommendations = self._generate_with_openai(problem_text)
            else:
                # Fallback to rule-based recommendations
                logger.warning("OpenAI API key not configured, using fallback recommendations")
                recommendations = self._generate_fallback_recommendations(problem_text)
            
            elapsed_time = time.time() - start_time
            logger.info(f"Generated recommendations in {elapsed_time:.2f} seconds")
            
            # Ensure response time is under 5 seconds
            if elapsed_time > self.max_response_time:
                logger.warning(f"Recommendation generation took {elapsed_time:.2f}s, exceeding {self.max_response_time}s limit")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            # Return fallback recommendations on error
            return self._generate_fallback_recommendations(problem_text)
    
    def _generate_with_openai(self, problem_text: str) -> List[Dict[str, str]]:
        """
        Generate recommendations using OpenAI API.
        
        Args:
            problem_text: The problem description
            
        Returns:
            List of recommendation dictionaries
        """
        try:
            import openai
            
            openai.api_key = self.api_key
            
            # Create a prompt for problem analysis
            prompt = self._create_prompt(problem_text)
            
            # Call OpenAI API with timeout
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that provides practical solutions to service-related problems. Provide 3-5 actionable recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7,
                timeout=4  # Leave 1 second buffer for processing
            )
            
            # Parse the response
            content = response.choices[0].message.content
            recommendations = self._parse_openai_response(content)
            
            return recommendations
            
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    def _create_prompt(self, problem_text: str) -> str:
        """
        Create a structured prompt for the AI model.
        
        Args:
            problem_text: The problem description
            
        Returns:
            Formatted prompt string
        """
        return f"""
A user has reported the following problem with a service:

"{problem_text}"

Please provide 3-5 practical and actionable recommendations to help resolve this issue. 
Format each recommendation as:

RECOMMENDATION [number]:
Title: [Brief title]
Description: [Detailed explanation]

Focus on solutions that are:
- Practical and actionable
- Specific to the problem described
- Easy to understand and implement
"""
    
    def _parse_openai_response(self, content: str) -> List[Dict[str, str]]:
        """
        Parse OpenAI response into structured recommendations.
        
        Args:
            content: Raw response from OpenAI
            
        Returns:
            List of recommendation dictionaries
        """
        recommendations = []
        lines = content.strip().split('\n')
        
        current_rec = {}
        for line in lines:
            line = line.strip()
            
            if line.startswith('Title:'):
                current_rec['title'] = line.replace('Title:', '').strip()
            elif line.startswith('Description:'):
                current_rec['description'] = line.replace('Description:', '').strip()
                
                # If we have both title and description, add to list
                if 'title' in current_rec and 'description' in current_rec:
                    recommendations.append(current_rec)
                    current_rec = {}
        
        # If parsing failed, create a single recommendation from the entire content
        if not recommendations:
            recommendations = [{
                'title': 'AI Recommendation',
                'description': content.strip()
            }]
        
        return recommendations
    
    def _generate_fallback_recommendations(self, problem_text: str) -> List[Dict[str, str]]:
        """
        Generate rule-based fallback recommendations when AI is unavailable.
        
        Args:
            problem_text: The problem description
            
        Returns:
            List of generic recommendation dictionaries
        """
        problem_lower = problem_text.lower()
        
        recommendations = []
        
        # Generic recommendations based on keywords
        if any(word in problem_lower for word in ['late', 'delay', 'time', 'slow']):
            recommendations.append({
                'title': 'Contact the Service Provider',
                'description': 'Reach out to the service provider directly to discuss the timing issue and request an updated schedule or explanation for the delay.'
            })
            recommendations.append({
                'title': 'Set Clear Expectations',
                'description': 'Communicate your time constraints clearly and ask for a realistic timeline that works for both parties.'
            })
        
        if any(word in problem_lower for word in ['quality', 'poor', 'bad', 'unsatisfied']):
            recommendations.append({
                'title': 'Document the Issues',
                'description': 'Take photos or detailed notes of the quality issues to share with the service provider for resolution.'
            })
            recommendations.append({
                'title': 'Request Corrections',
                'description': 'Politely explain the quality concerns and request that the provider address them or redo the work to meet your expectations.'
            })
        
        if any(word in problem_lower for word in ['cost', 'price', 'expensive', 'charge']):
            recommendations.append({
                'title': 'Review the Agreement',
                'description': 'Check your original service agreement or quote to verify the pricing and identify any discrepancies.'
            })
            recommendations.append({
                'title': 'Negotiate or Clarify',
                'description': 'Discuss the pricing concerns with the provider and ask for a detailed breakdown of charges.'
            })
        
        if any(word in problem_lower for word in ['communication', 'respond', 'contact', 'reply']):
            recommendations.append({
                'title': 'Try Multiple Contact Methods',
                'description': 'Attempt to reach the provider through different channels (email, phone, platform messaging) to ensure your message is received.'
            })
            recommendations.append({
                'title': 'Set Communication Expectations',
                'description': 'Request a preferred method and timeframe for communication to avoid future issues.'
            })
        
        # If no specific keywords matched, provide general recommendations
        if not recommendations:
            recommendations = [
                {
                    'title': 'Contact the Service Provider',
                    'description': 'Reach out to the service provider directly to discuss your concerns and work towards a resolution.'
                },
                {
                    'title': 'Document Everything',
                    'description': 'Keep detailed records of all communications, agreements, and issues for reference and potential dispute resolution.'
                },
                {
                    'title': 'Review Platform Policies',
                    'description': 'Check the platform\'s terms of service and dispute resolution procedures for guidance on handling service issues.'
                },
                {
                    'title': 'Provide Constructive Feedback',
                    'description': 'Share specific, actionable feedback with the provider to help them understand and address your concerns.'
                }
            ]
        
        return recommendations[:5]  # Return maximum 5 recommendations

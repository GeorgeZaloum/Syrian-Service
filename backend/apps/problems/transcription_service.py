"""
Voice Transcription Service for converting audio to text.
"""
from typing import Optional
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
import logging

logger = logging.getLogger(__name__)


class VoiceTranscriptionService:
    """Service for transcribing voice recordings to text."""
    
    # Supported audio formats
    SUPPORTED_FORMATS = [
        'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/wave',
        'audio/x-wav', 'audio/ogg', 'audio/webm', 'audio/mp4',
        'audio/m4a', 'audio/x-m4a'
    ]
    
    # Maximum file size (10 MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
    
    def validate_audio_file(self, audio_file: UploadedFile) -> tuple[bool, Optional[str]]:
        """
        Validate the uploaded audio file.
        
        Args:
            audio_file: The uploaded audio file
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if file exists
        if not audio_file:
            return False, "No audio file provided"
        
        # Check file size
        if audio_file.size > self.MAX_FILE_SIZE:
            max_size_mb = self.MAX_FILE_SIZE / (1024 * 1024)
            return False, f"Audio file size exceeds maximum limit of {max_size_mb}MB"
        
        # Check file format
        content_type = audio_file.content_type
        if content_type not in self.SUPPORTED_FORMATS:
            return False, f"Unsupported audio format: {content_type}. Supported formats: MP3, WAV, OGG, WEBM, M4A"
        
        return True, None
    
    def transcribe_audio(self, audio_file: UploadedFile) -> str:
        """
        Transcribe audio file to text.
        
        Args:
            audio_file: The uploaded audio file
            
        Returns:
            Transcribed text
            
        Raises:
            ValueError: If audio file validation fails
            Exception: If transcription fails
        """
        # Validate audio file
        is_valid, error_message = self.validate_audio_file(audio_file)
        if not is_valid:
            raise ValueError(error_message)
        
        try:
            if self.api_key:
                # Use OpenAI Whisper API for transcription
                transcription = self._transcribe_with_whisper(audio_file)
            else:
                # Fallback error when API key is not configured
                logger.error("OpenAI API key not configured for transcription")
                raise ValueError(
                    "Voice transcription is currently unavailable. "
                    "Please use text input or contact support."
                )
            
            return transcription
            
        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            raise Exception(
                f"Failed to transcribe audio: {str(e)}. "
                "Please try again or use text input instead."
            )
    
    def _transcribe_with_whisper(self, audio_file: UploadedFile) -> str:
        """
        Transcribe audio using OpenAI Whisper API.
        
        Args:
            audio_file: The uploaded audio file
            
        Returns:
            Transcribed text
        """
        try:
            import openai
            
            openai.api_key = self.api_key
            
            # Reset file pointer to beginning
            audio_file.seek(0)
            
            # Call Whisper API
            response = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="en"  # Can be made configurable
            )
            
            transcription = response.get('text', '').strip()
            
            if not transcription:
                raise ValueError("Transcription resulted in empty text")
            
            logger.info(f"Successfully transcribed audio file: {audio_file.name}")
            return transcription
            
        except ImportError:
            logger.error("OpenAI library not installed. Install with: pip install openai")
            raise Exception("Voice transcription service is not properly configured")
        except Exception as e:
            logger.error(f"Whisper API error: {str(e)}")
            raise

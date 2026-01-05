# Problem Reporting API

This module handles user problem reporting with AI-powered recommendations and voice transcription support.

## Features

- Text-based problem submission
- Voice-based problem submission with automatic transcription
- AI-powered solution recommendations (using OpenAI GPT-3.5)
- Fallback recommendations when AI is unavailable
- User-specific problem history
- Response time under 5 seconds

## API Endpoints

### Create Problem Report
**POST** `/api/problems/create/`

Submit a new problem report with either text or voice input.

**Request (Text Input):**
```json
{
  "input_type": "TEXT",
  "problem_text": "The service provider was late and didn't complete the work properly."
}
```

**Request (Voice Input):**
```
Content-Type: multipart/form-data

input_type: VOICE
audio_file: [audio file]
```

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "input_type": "TEXT",
  "problem_text": "The service provider was late and didn't complete the work properly.",
  "audio_file": null,
  "recommendations": [
    {
      "title": "Contact the Service Provider",
      "description": "Reach out to the service provider directly to discuss the timing issue..."
    },
    {
      "title": "Document the Issues",
      "description": "Take photos or detailed notes of the quality issues..."
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### List Problem Reports
**GET** `/api/problems/`

Get all problem reports for the authenticated user.

**Response:**
```json
[
  {
    "id": 1,
    "user_email": "user@example.com",
    "input_type": "TEXT",
    "problem_text": "The service provider was late...",
    "recommendation_count": 3,
    "created_at": "2024-01-15T10:30:00Z"
  }
]
```

### Get Problem Report Detail
**GET** `/api/problems/{id}/`

Get detailed information about a specific problem report.

**Response:**
```json
{
  "id": 1,
  "user": 1,
  "user_email": "user@example.com",
  "user_name": "John Doe",
  "input_type": "TEXT",
  "problem_text": "The service provider was late and didn't complete the work properly.",
  "audio_file": null,
  "recommendations": [
    {
      "title": "Contact the Service Provider",
      "description": "Reach out to the service provider directly..."
    }
  ],
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

## Configuration

### Environment Variables

Add the following to your `.env` file:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
```

### Audio File Requirements

- **Supported formats:** MP3, WAV, OGG, WEBM, M4A
- **Maximum file size:** 10 MB
- **Language:** English (configurable)

## Services

### AIRecommendationService

Generates AI-powered recommendations for user problems.

- Uses OpenAI GPT-3.5 Turbo for intelligent recommendations
- Falls back to rule-based recommendations if API is unavailable
- Ensures response time under 5 seconds
- Returns 3-5 actionable recommendations

### VoiceTranscriptionService

Transcribes voice recordings to text.

- Uses OpenAI Whisper API for accurate transcription
- Validates audio file format and size
- Handles transcription errors gracefully
- Supports multiple audio formats

### ProblemReportService

Manages the problem report lifecycle.

- Coordinates transcription and recommendation generation
- Creates and stores problem reports
- Enforces user-level access control
- Provides problem history retrieval

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK:** Successful retrieval
- **201 Created:** Problem report created successfully
- **400 Bad Request:** Validation error (invalid input)
- **401 Unauthorized:** Authentication required
- **404 Not Found:** Problem report not found
- **500 Internal Server Error:** Processing error

## Testing

To test the API:

1. Ensure OpenAI API key is configured
2. Authenticate as a regular user
3. Submit a problem report via text or voice
4. Verify recommendations are returned within 5 seconds
5. Check problem history

## Dependencies

- `openai>=1.3.0` - OpenAI API client for GPT and Whisper

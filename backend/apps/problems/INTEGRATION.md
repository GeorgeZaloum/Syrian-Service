# Problem Reporting Integration Guide

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install the `openai` package required for AI recommendations and voice transcription.

### 2. Configure Environment Variables

Add the following to your `.env` file:

```bash
# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
```

**Note:** The system will work without an API key but will use fallback rule-based recommendations instead of AI-powered ones.

### 3. Run Migrations

```bash
python manage.py migrate problems
```

This creates the `problem_reports` table in your database.

### 4. Verify Installation

Check that the problems app is properly configured:

```bash
python manage.py check
```

## Usage Examples

### Text-Based Problem Report (cURL)

```bash
curl -X POST http://localhost:8000/api/problems/create/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "TEXT",
    "problem_text": "The service provider was late and the work quality was poor."
  }'
```

### Voice-Based Problem Report (cURL)

```bash
curl -X POST http://localhost:8000/api/problems/create/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "input_type=VOICE" \
  -F "audio_file=@/path/to/audio.mp3"
```

### List Problem Reports

```bash
curl -X GET http://localhost:8000/api/problems/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get Problem Report Detail

```bash
curl -X GET http://localhost:8000/api/problems/1/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Frontend Integration

### JavaScript/TypeScript Example

```typescript
// Submit text problem
async function submitTextProblem(problemText: string, token: string) {
  const response = await fetch('http://localhost:8000/api/problems/create/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      input_type: 'TEXT',
      problem_text: problemText,
    }),
  });
  
  return await response.json();
}

// Submit voice problem
async function submitVoiceProblem(audioFile: File, token: string) {
  const formData = new FormData();
  formData.append('input_type', 'VOICE');
  formData.append('audio_file', audioFile);
  
  const response = await fetch('http://localhost:8000/api/problems/create/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
    body: formData,
  });
  
  return await response.json();
}

// Get problem history
async function getProblemHistory(token: string) {
  const response = await fetch('http://localhost:8000/api/problems/', {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  return await response.json();
}
```

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (views.py)                  │
│  - ProblemReportCreateView                              │
│  - ProblemReportListView                                │
│  - ProblemReportDetailView                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              Business Logic (services.py)                │
│  - ProblemReportService                                 │
│    • create_problem_report()                            │
│    • get_user_problem_reports()                         │
│    • get_problem_report_by_id()                         │
└─────────────────────────────────────────────────────────┘
                          │
                ┌─────────┴─────────┐
                ▼                   ▼
┌──────────────────────┐  ┌──────────────────────┐
│   AI Service         │  │ Transcription Service│
│ (ai_service.py)      │  │(transcription_service│
│                      │  │        .py)          │
│ - OpenAI GPT-3.5     │  │ - OpenAI Whisper     │
│ - Fallback rules     │  │ - Audio validation   │
└──────────────────────┘  └──────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                Data Layer (models.py)                    │
│  - ProblemReport Model                                  │
└─────────────────────────────────────────────────────────┘
```

## Key Features

1. **Dual Input Support**: Accept both text and voice input
2. **AI-Powered Recommendations**: Generate intelligent solutions using GPT-3.5
3. **Fallback System**: Rule-based recommendations when AI is unavailable
4. **Voice Transcription**: Automatic audio-to-text conversion using Whisper
5. **User Privacy**: Users can only access their own problem reports
6. **Performance**: Response time under 5 seconds
7. **Error Handling**: Graceful degradation and user-friendly error messages

## Troubleshooting

### OpenAI API Errors

If you encounter OpenAI API errors:

1. Verify your API key is correct in `.env`
2. Check your OpenAI account has sufficient credits
3. Ensure you have network connectivity
4. The system will automatically fall back to rule-based recommendations

### Audio Upload Issues

If audio uploads fail:

1. Check file size is under 10 MB
2. Verify file format is supported (MP3, WAV, OGG, WEBM, M4A)
3. Ensure `MEDIA_ROOT` is properly configured in settings
4. Check file permissions on the media directory

### Slow Response Times

If recommendations take longer than 5 seconds:

1. Check your internet connection to OpenAI API
2. Consider using a faster OpenAI model
3. Implement caching for common problems
4. Monitor OpenAI API status

## Security Considerations

1. **Authentication Required**: All endpoints require JWT authentication
2. **User Isolation**: Users can only access their own problem reports
3. **File Validation**: Audio files are validated for size and format
4. **API Key Security**: OpenAI API key stored in environment variables
5. **Input Sanitization**: All user input is validated and sanitized

## Performance Optimization

1. **Async Processing**: Consider using Celery for long-running AI tasks
2. **Caching**: Cache common problem patterns and recommendations
3. **Database Indexing**: Indexes on user and created_at fields
4. **File Storage**: Use cloud storage (S3) for audio files in production
5. **Rate Limiting**: Implement rate limiting to prevent abuse

## Next Steps

1. Set up Celery for async processing (optional)
2. Implement caching with Redis (optional)
3. Add analytics tracking for problem patterns
4. Create admin dashboard for problem monitoring
5. Implement problem categorization and tagging

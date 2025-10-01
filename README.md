# SubVoice API

## 🎯 Генерація аудіо через ElevenLabs API

### 📡 API Endpoint
```
POST /api/generate-audio
```

### 📋 Параметри запиту
```json
{
  "api_key": "YOUR_ELEVENLABS_API_KEY",
  "text": "Text to convert to speech",
  "voice_id": "VOICE_ID",
  "stability": 0.5,
  "style": 0.3
}
```

### 📤 Відповідь
```json
{
  "success": true,
  "audio_base64": "base64_encoded_audio",
  "timestamps": {
    "characters": ["H", "e", "l", "l", "o"],
    "character_start_times_seconds": [0.0, 0.1, 0.2, 0.3, 0.4],
    "character_end_times_seconds": [0.1, 0.2, 0.3, 0.4, 0.5]
  }
}
```

### 🚀 Деплой на Vercel
1. Підключіть репозиторій до Vercel
2. Автоматичний деплой
3. Отримайте URL: `https://your-project.vercel.app`

### 💰 Вартість
- **Безкоштовно** до 100GB bandwidth/місяць
- **Безкоштовно** до 100GB-hours execution/місяць

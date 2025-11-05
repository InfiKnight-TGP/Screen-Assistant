# Screen Assistant 🎙️🖥️📸

An AI-powered voice assistant that can see your screen and webcam, allowing you to have natural conversations about what you're working on or what's visible in your environment.

## Features

- 🎤 **Voice Input**: Continuous listening with automatic speech recognition using Whisper
- 🖥️ **Screen Capture**: Captures and analyzes your screen content
- 📸 **Webcam Integration**: Accesses webcam feed for visual context
- 🤖 **AI Vision**: Uses OpenAI's GPT-4 with vision capabilities to understand both screen and webcam images
- 🔊 **Text-to-Speech**: Responds with natural-sounding voice using OpenAI's TTS
- 💬 **Conversational**: Maintains chat history for contextual conversations

## Prerequisites

- **Python 3.10+** (Python 3.9 reached end of life in October 2025)
- OpenAI API key
- FFmpeg installed (required by Whisper for audio decoding)
- Webcam
- Microphone

## Dependencies

Core dependencies include:

- `langchain` / `langchain-core` / `langchain-community` / `langchain-openai`
- `opencv-python` - Webcam and image processing
- `mss` - Fast screen capture
- `numpy` - Array operations
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pyaudio` - Audio input/output
- `SpeechRecognition` - Mic handling + Whisper integration
- `openai-whisper` - Local Whisper model (requires FFmpeg)
- FFmpeg (system dependency)

```bash
python main.py
```

1. Start the webcam stream
2. Begin listening for voice input
3. Display two windows showing the webcam feed and screen capture
4. Respond to your voice commands with contextual awareness of both your screen and webcam
**To exit**: Press `Q` or `ESC` in any of the display windows

## How It Works
1. **Continuous Listening**: The assistant listens in the background for your voice input
2. **Multi-Modal Capture**: When you speak, it captures both your screen and webcam frame
3. **AI Processing**: The text prompt and images are sent to the model for analysis
4. **Voice Response**: The AI's response is converted to speech and played back to you

## Dependencies

Core dependencies include:

- `langchain>=1.0.0` - LLM orchestration framework
- `langchain-core>=1.0.0` - Core LangChain functionality
- `langchain-community>=0.4.0` - Community integrations for LangChain
- `langchain-openai>=1.0.0` - OpenAI integration for LangChain
- `opencv-python` - Webcam and image processing
- `mss` - Fast screen capture
- `numpy>=2.1.0` - Array operations
- `openai>=2.7.0` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pyaudio` - Audio playback
- `speechrecognition` - Voice recognition library
- `soundfile` - Audio file processing dependency

**Complete requirements.txt:**
```
langchain>=1.0.0
langchain-core>=1.0.0
langchain-community>=0.4.0
langchain-openai>=1.0.0
opencv-python
mss
numpy>=2.1.0
openai>=2.7.0
python-dotenv
pyaudio
SpeechRecognition
soundfile
```

## Model Configuration

The assistant uses:
- **Vision Model**: GPT-5-mini (with fallback to GPT-4o-mini, then GPT-4o)
- **Speech Recognition**: Whisper base model (via SpeechRecognition library)
- **Text-to-Speech**: OpenAI TTS-1 with "alloy" voice

## Troubleshooting

### ModuleNotFoundError: No module named 'langchain.prompts'
This error occurs with LangChain v1.0+. Update your imports:
- Change `from langchain.prompts import` to `from langchain_core.prompts import`
- Change `from langchain.schema.messages import` to `from langchain_core.messages import`

### Whisper / FFmpeg errors
- Error: `ModuleNotFoundError: No module named 'whisper'` or `'openai_whisper'`
	- Install the package: `pip install openai-whisper`
- Error: `ffmpeg not found`
	- Install FFmpeg and ensure it's on your PATH.
		- Windows (PowerShell): `winget install Gyan.FFmpeg` or `choco install ffmpeg -y`
		- macOS: `brew install ffmpeg`
		- Ubuntu/Debian: `sudo apt-get install -y ffmpeg`

### No audio output
- Ensure PyAudio is properly installed
- Check your system's audio output settings
- On Windows, you may need to install PyAudio from a wheel file

### Webcam not found
- Verify your webcam is connected and not in use by another application
- Check webcam permissions in your OS settings

### "Didn't catch that" messages
- Speak clearly and ensure your microphone is working
- Check microphone permissions in your OS settings
- Adjust ambient noise calibration by restarting the application in a quieter environment

### API errors
- Verify your OpenAI API key is valid and properly set in `.env`
- Ensure you have sufficient API credits
- Check your internet connection
- Note: GPT-5-mini may not be available to all accounts; the code will automatically fall back to GPT-4o-mini or GPT-4o

## API Costs

This application uses several OpenAI APIs, which incur costs based on usage:

### Model Pricing (per 1 million tokens)

**GPT-5 mini** (Primary model):
- Input: $0.25 per 1M tokens
- Cached input: $0.025 per 1M tokens
- Output: $2.00 per 1M tokens

**GPT-4o-mini** (First fallback):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens

**GPT-4o** (Second fallback):
- Input: $2.50 per 1M tokens
- Output: $10.00 per 1M tokens

**TTS (Text-to-Speech)**:
- $0.015 per 1,000 characters (~$15 per 1M characters)

### Vision API Considerations

- Images are processed at high detail, which significantly affects token count
- Each interaction sends 2 images (screen + webcam) to the API
- Image tokens vary based on resolution and detail level (typically 500-2000 tokens per image)

### Cost Estimate Per Interaction

Assuming GPT-5 mini is used:

**Input costs:**
- Text prompt: ~50-200 tokens ($0.000012-$0.00005)
- Screen image: ~1000-2000 tokens ($0.00025-$0.0005)
- Webcam image: ~1000-2000 tokens ($0.00025-$0.0005)
- Total input: ~$0.0005-$0.0012 per request

**Output costs:**
- Response: ~100-300 tokens ($0.0002-$0.0006)
- TTS: ~100-300 characters ($0.0015-$0.0045)

**Total per interaction: ~$0.003-$0.007** (approximately $0.005 or half a cent per request)

### Usage Scenarios

- **Light use** (50 interactions/day): ~$0.25/day or $7.50/month
- **Moderate use** (200 interactions/day): ~$1/day or $30/month
- **Heavy use** (500 interactions/day): ~$2.50/day or $75/month

**Note**: The code uses Whisper through the SpeechRecognition library's local implementation, not OpenAI's Whisper API, so there are no API costs for speech recognition.

### Cost Optimization Tips

1. **Use caching**: GPT-5 mini offers 90% discount on cached input tokens ($0.025 vs $0.25)
2. **Reduce image frequency**: Consider capturing images only when needed rather than continuously
3. **Shorter responses**: Keep system prompts concise to minimize output tokens
4. **Monitor usage**: Regularly check your OpenAI API usage dashboard

Since the assistant runs continuously and processes every voice command with two images, costs can accumulate. Monitor your OpenAI API usage dashboard regularly.

## Security & Privacy

**Data Handling:**
- Screenshots and webcam frames are Base64-encoded for transport (encoding, not encryption); data is sent over HTTPS
- Images are kept temporarily in memory only for the duration needed to send them to the language model
- No screenshots or webcam images are stored persistently on disk
- Conversation history is maintained in memory and cleared when the application exits

**Privacy Considerations:**
- The application captures your screen and webcam continuously while running
- All captured images are sent to OpenAI's API for processing
- OpenAI's data usage policies apply to all transmitted data
- Be mindful of sensitive information visible on your screen or in your environment

 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- OpenAI for GPT-5 and Whisper models
- LangChain for the orchestration framework
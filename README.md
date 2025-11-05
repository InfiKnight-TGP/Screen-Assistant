# Screen Assistant 🎙️🖥️📸

An intelligent real‑time multimodal assistant that **sees your screen**, **understands your environment through webcam**, and **converses with you through voice** — designed to act as your always‑available AI co‑pilot for productivity.

> **Future Vision 🚀**: A portable `.exe` / desktop app with minimal UI, hotkey & voice‑activated startup, API setup prompt, and full privacy controls (mic, webcam, screen access toggles).

---

## ✨ Key Features

### 🗣️ Voice Interaction

* Always‑listening mode
* Whisper‑based speech recognition
* Natural voice replies using OpenAI TTS

### 👁️ Multimodal Perception

* **Screen Capture**: Understands what's happening on your screen
* **Webcam Vision**: Interprets real‑world context
* **GPT‑5 Vision** for true multimodal reasoning

### 🤖 Smart AI Capabilities

* Understands tasks, code, UI, and real‑world visuals
* Maintains conversation context
* Can answer, explain, and assist with on‑screen work

### 🎧 System Integration

* Mic + Webcam support
* Real‑time screen stream
* Continuous voice detection

### 🎮 User Experience

* Live screen + webcam preview
* Easy voice command flow
* Press **Q / ESC** to exit

---

## 🏗️ Tech Stack

| Component          | Technology                                 |
| ------------------ | ------------------------------------------ |
| Language           | Python 3.10+                               |
| LLM                | GPT‑5‑mini → fallback GPT‑4o‑mini / GPT‑4o |
| Speech‑to‑Text     | Whisper (local)                            |
| TTS                | OpenAI TTS‑1 (Alloy voice)                 |
| Vision             | OpenAI Vision API + OpenCV                 |
| Screen Capture     | MSS                                        |
| Audio Interface    | PyAudio                                    |
| Environment Config | python‑dotenv                              |

---

## 🧰 Requirements

* ✅ Python 3.10+
* ✅ FFmpeg installed
* ✅ Microphone + Webcam
* ✅ OpenAI API Key

Install FFmpeg:

```bash
# Windows
winget install Gyan.FFmpeg
# Mac
brew install ffmpeg
# Linux
sudo apt install ffmpeg
```

---

## 📦 Installation

```bash
git clone <repo_url>
cd Screen-Assistant
pip install -r requirements.txt
```

Add your API key:

```bash
echo "OPENAI_API_KEY=your_key" > .env
```

Run:

```bash
python main.py
```

---

## ▶️ How It Works

1. Listens for voice commands
2. Captures screen & webcam when user speaks
3. Sends voice → text + images → GPT‑5
4. Speaks back response aloud
5. UI windows show:

   * 👁️ Webcam feed
   * 🖥️ Screen feed

Press **ESC / Q** to quit.

---

## ⚙️ Configuration

Default model hierarchy:

```
GPT‑5‑mini
⬇️ fallback
GPT‑4o‑mini
⬇️ fallback
GPT‑4o
```

You may modify: voice, model, resolution, frequency, hotkey behaviour.

---

## 💰 Token & Cost Notes

Average usage bundle per command:

* 2 images (screen + webcam)
* Voice input + voice output

**Estimated: ~$0.003 – $0.007 per interaction**

Optimizations planned:

* 🔁 Caching
* 🎚️ Quality scaling
* 🕵🏻‍♂️ On‑demand capture instead of always

---

## 🛡️ Privacy & Data

✔️ Images processed only in‑memory
✔️ Nothing stored locally
✔️ All communication encrypted (HTTPS)
❗ OpenAI receives image + audio for inference

> Future `.exe` version will allow **granular permission control** for camera/mic/screen.

---

## 🧠 Future Enhancements

### 📦 Product Roadmap

* ✅ Move from script → GUI app
* 🔒 Permissions dashboard (mic/webcam/screen)
* 🎤 Hotkey + wake‑phrase activation ("Hey Assist")
* 💻 Full tray background mode
* 🧠 Memory toggle per session
* 💬 On‑screen chat overlay
* 🧵 Always‑on context threads
* 📡 Local model support when possible

### 🤖 Automation Features

* Screen OCR & clickable actions
* Auto‑explain on‑screen errors
* Code assistant mode
* System automation (shortcuts)

---

## 📜 License

MIT

## 🤝 Contributing

PRs welcome — let's build the AI desktop assistant of the future.

---

> **Built with ❤️ to make your computer truly understand you.**

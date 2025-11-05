import base64
import os
from threading import Lock, Thread
import cv2
import mss
import numpy as np
import openai
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from pyaudio import PyAudio, paInt16
from speech_recognition import Microphone, Recognizer, UnknownValueError


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# 📸 Webcam Stream Class
class WebcamStream:
    def __init__(self):
        self.stream = cv2.VideoCapture(0)
        _, self.frame = self.stream.read()
        self.running = False
        self.lock = Lock()

    def start(self):
        if self.running:
            return self
        self.running = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.running:
            _, frame = self.stream.read()
            with self.lock:
                self.frame = frame

    def read(self, encode=False):
        with self.lock:
            frame = self.frame.copy()
        if encode:
            _, buffer = cv2.imencode(".jpeg", frame)
            return base64.b64encode(buffer)
        return frame

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()
        self.stream.release()


# 🖥️ Screen capture function
def capture_screen(encode=False):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))[:, :, :3]
    if encode:
        _, buffer = cv2.imencode(".jpeg", screenshot)
        return base64.b64encode(buffer)
    return screenshot


# 🤖 Assistant Class
class Assistant:
    def __init__(self, model):
        self.chain = self._create_inference_chain(model)

    def answer(self, prompt, screen_img, webcam_img):
        if not prompt:
            return
        print("Prompt:", prompt)
        try:
            response = self.chain.invoke(
                {
                    "prompt": prompt,
                    "screen_base64": screen_img.decode(),
                    "webcam_base64": webcam_img.decode(),
                },
                config={"configurable": {"session_id": "unused"}},
            ).strip()
            print("Response:", response)
            if response:
                self._tts(response)
        except Exception as e:
            print("❌ Model invocation error:", e)

    def _tts(self, response):
        player = PyAudio().open(format=paInt16, channels=1, rate=24000, output=True)
        with openai.audio.speech.with_streaming_response.create(
            model="tts-1", voice="alloy", response_format="pcm", input=response
        ) as stream:
            for chunk in stream.iter_bytes(chunk_size=1024):
                player.write(chunk)

    def _create_inference_chain(self, model):
        SYSTEM_PROMPT = """
        You are a visual + voice assistant. You get user's voice input, their screen and webcam.
        Use this to answer short, friendly responses. No emojis. No long stories. Just helpful, witty answers.
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=SYSTEM_PROMPT),
                MessagesPlaceholder(variable_name="chat_history"),
                (
                    "human",
                    [
                        {"type": "text", "text": "{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{screen_base64}",
                        },
                        {
                            "type": "image_url",
                            "image_url": "data:image/jpeg;base64,{webcam_base64}",
                        },
                    ],
                ),
            ]
        )
        chain = prompt_template | model | StrOutputParser()
        return RunnableWithMessageHistory(
            chain,
            lambda _: ChatMessageHistory(),
            input_messages_key="prompt",
            history_messages_key="chat_history",
        )


# ✅ Load OpenAI Model (GPT-5 mini with fallbacks)
try:
    model = ChatOpenAI(model="gpt-5-mini", temperature=0.7, max_tokens=1000)
    print("✅ Using GPT-5 mini")
except Exception as e:
    print("⚠️ GPT-5 mini not available, trying GPT-4o-mini:", e)
    try:
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7, max_tokens=1000)
        print("✅ Using GPT-4o-mini")
    except Exception as e2:
        print("⚠️ GPT-4o-mini not available, falling back to GPT-4o:", e2)
        model = ChatOpenAI(model="gpt-4o", temperature=0.7, max_tokens=1000)
        print("✅ Using GPT-4o")


assistant = Assistant(model)
webcam = WebcamStream().start()


# 🎤 Audio Callback Function
def audio_callback(recognizer, audio):
    try:
        prompt = recognizer.recognize_whisper(audio, model="base", language="english")
        screen_img = capture_screen(encode=True)
        webcam_img = webcam.read(encode=True)
        assistant.answer(prompt, screen_img, webcam_img)
    except UnknownValueError:
        print("Didn't catch that.")
    except Exception as e:
        print("❌ Error:", e)


# 🎙️ Mic Listening
recognizer = Recognizer()
microphone = Microphone()
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)


stop_listening = recognizer.listen_in_background(microphone, audio_callback)


try:
    while True:
        # Show both webcam and screen for visual reference
        cv2.imshow("Webcam", webcam.read())
        cv2.imshow("Screen", capture_screen())
        if cv2.waitKey(1) in [27, ord("q")]:
            break
finally:
    webcam.stop()
    cv2.destroyAllWindows()
    stop_listening(wait_for_stop=False)
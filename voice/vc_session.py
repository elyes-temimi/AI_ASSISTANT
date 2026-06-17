from voice.stt import listen
from voice.tts import speak
from voice.state import voice_state


def start_voice_chat(agent):
    if voice_state.enter_vc():
        print("⚠️ VC already active")
        return

    print("🔊 Voice chat started (say 'exit voice')")
    
    try:
        
        while True:
            print("🎤 Listening...")
            user_text = listen()["text"]

            if not user_text:
                continue

            user_text = user_text.lower().strip()
            print("Heard:", user_text)

            # EXIT VC
            if "exit voice" in user_text:
                print("🔕 Voice chat stopped")
                break

                # NORMAL CONVERSATION (NO WAKE WORD REQUIRED)
            response = agent.respond(user_text)
                
            reply = response

            print("Assistant:", reply)
            speak(reply)
    finally:
        voice_state.exit_vc()

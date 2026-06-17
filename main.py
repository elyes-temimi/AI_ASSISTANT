from agent.agent import AssistantAgent
from memory.short_term import ShortTermMemory
from config import DEFAULT_PERSONALITY
from voice.vc_session import start_voice_chat
import threading
from voice.wake_listener import passive_listen_for_wake_word
from voice.vc_session import start_voice_chat
from voice.state import voice_state


def main():
    memory = ShortTermMemory()
    agent = AssistantAgent(
        personality_file=f"personalities/{DEFAULT_PERSONALITY}.json",
        memory=memory
    )

    threading.Thread(
        target=passive_listen_for_wake_word,
        args=(agent, start_voice_chat),
        daemon=True
    ).start()

    print("AI Assistant ready.")
    print("Type 'VC' or say 'Hey Nova'")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "vc":
            if voice_state.enter_vc():
                start_voice_chat(agent)
                voice_state.exit_vc()
            else:
                print("⚠️ VC already active")
                
        response = agent.respond(user_input)
        print("Assistant:", response)

if __name__ == "__main__":
    main()

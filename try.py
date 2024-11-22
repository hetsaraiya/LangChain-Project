from app.handle_llm import check_greeting

new= check_greeting("Hello how are you doing today?")
print(new.content.strip())
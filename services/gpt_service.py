from ai_open import chat_gpt

async def ask_gpt(message_list, bot):
    return await chat_gpt.request(message_list, bot)
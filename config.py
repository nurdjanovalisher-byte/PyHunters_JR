import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PROXY = os.getenv('PROXY')
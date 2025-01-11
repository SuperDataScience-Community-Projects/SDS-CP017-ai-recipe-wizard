from src.RecipeWizard import startWizard
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# print(f"OPEN KEY ::  {os.getenv('OPENAI_API_KEY')}")
 
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":  
    # print(f"OPEN AI KEY: {os.environ['OPENAI_API_KEY']}")
    startWizard('openai', 'openai')

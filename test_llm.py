import config
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    temperature=0.0,
    api_key=config.GEMINI_API_KEY
)

print(llm.invoke("hello").content)

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# LLM and embedding setup
llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY, temperature=0.0
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001", google_api_key=GOOGLE_API_KEY
)

persist_directory = "chroma_db"
vector_store = Chroma(
    persist_directory=persist_directory, embedding_function=embedding_model
)

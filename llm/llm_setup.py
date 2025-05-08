# import google.generativeai as genai

# from config.load import GOOGLE_API_KEY


# genai.configure(api_key=GOOGLE_API_KEY)
# llm = genai.GenerativeModel(
#             model_name="gemini-2.0-flash"
#         )

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from config.load import GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY
)

def get_qa_chain(store):
    return RetrievalQA.from_chain_type(llm=llm, retriever=store.as_retriever())

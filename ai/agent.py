import os

from decouple import config
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from ai import prompts


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class AIBot:

    def __init__(self):
            self.__chat = ChatGroq(model='llama-3.3-70b-versatile')
            self.__embedding  = HuggingFaceEmbeddings()
            self.__vector_store = Chroma(
                persist_directory='ai/rag/rag_db',
                embedding_function=self.__embedding,
                collection_name='curriculo_marcus'
            )
            self.__retriever = self.__vector_store.as_retriever()

    def invoke(self, question, history_message):
        chat_history = []

        for msg in history_message:
            if msg.user_input:
                chat_history.append(HumanMessage(content=msg.user_input))
            elif msg.bot_response: 
                chat_history.append(AIMessage(content=msg.bot_response))

        docs = self.__retriever.invoke(question)
        context_text = "\n\n".join([doc.page_content for doc in docs])

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=prompts.SYSTEM_PROMPT.format(context_text=context_text)),
            *chat_history,
            HumanMessagePromptTemplate.from_template("{question}")
        ])

        chain = prompt | self.__chat | StrOutputParser()
        response = chain.invoke({'question': question})

        return response

from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import( FAISS_INDEX_PATH, EMBEDDING_MODEL, OLLAMA_MODEL, OLLAMA_OPTIONS, RETRIEVER_K)
from prompt import RNCP_PROMPT

def load_vectorstore():
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vectorestore = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings, 
        allow_dangerous_deserialization=True
    )
    print( "Ok vectorestore loaded")

    return vectorestore


def build_retriever(vectorstore):
    llm = OllamaLLM(model=OLLAMA_MODEL, options=OLLAMA_OPTIONS)
    retriever = vectorstore.as_retriever(search_kwargs={"k": RETRIEVER_K})
    
    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])
   
    
    chain = (
        {"context" : retriever | format_docs, "question": RunnablePassthrough()}
        | RNCP_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain, retriever

def build_rag_chain():
    vectorstore = load_vectorstore()
    chain = build_retriever(vectorstore)
    return chain

def ask(chain, question):
    result = chain.invoke(question)
    return result
# src/interface.py
import chainlit as cl
import sys
sys.path.insert(0, 'src')

from retrieval import build_rag_chain, ask

@cl.on_chat_start
async def on_chat_start():
    msg = cl.Message(content="Chargement du référentiel RNCP...")
    await msg.send()
    
    try :
        chain, _ = build_rag_chain()
        cl.user_session.set("chain", chain)
        msg.content = "Prêt ! Décris ton projet et je t'indique les compétences RNCP couvertes."
        
    except RuntimeError as e:
        msg.content = str(e)
    
    await msg.update()

@cl.on_message
async def on_message(message: cl.Message):
    chain = cl.user_session.get("chain")

    if chain is None:
        await cl.Message(content="L'assistant n'est pas initialisé. Recharge la page.").send()
        return
    
    msg = cl.Message(content="")
    await msg.send()
    
    try:
        async for chunk in chain.astream({"question": message.content}):
            await msg.stream_token(chunk)
    except Exception as e:
        msg.content = f" Erreur lors de la génération : {e}\nVérifie qu'Ollama est bien lancé."

    await msg.update()
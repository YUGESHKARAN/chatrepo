from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import create_csv_agent
import os
import openai


import chainlit as cl
from langchain.agents import initialize_agent,Tool,AgentExecutor   


#os.environ['OPENAI_API_KEY'] = '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' #roshinii

os.environ['OPENAI_API_KEY'] = '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' #charan

Greeting_sent = False

@cl.on_chat_start
def start():
    global Greeting_sent
    Greeting_sent=False
   
    llm=OpenAI(temperature=0.5, streaming=True,)

    agent =create_csv_agent(
        llm,
        ["job1.csv","job2.csv","guidances.csv","technical1.csv","technical2.csv","PGRKAM_Register.csv",],
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=False,  ### IMPORTANT
    )

    cl.user_session.set("agent", agent)
    

@cl.on_message
async def main(message):
    global Greeting_sent

    agent = cl.user_session.get("agent")  # type: AgentExecutor
    cb = cl.LangchainCallbackHandler(stream_final_answer=True)
    await cl.make_async(agent.run)(message, callbacks=[cb])
    
    if not Greeting_sent:
        await cl.Message(content= "\n How can I assist you today? \n -Looking for job. \n -Looking for skill development. \n-Looking for foreign counselling & study abroad guidance.").send()
        Greeting_sent = True
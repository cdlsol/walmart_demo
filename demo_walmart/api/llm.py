from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
from db import engine
from langchain.prompts import PromptTemplate


load_dotenv()

db = SQLDatabase(engine)
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

sql_agent_prompt = PromptTemplate(
    template="""
    You are an agent designed to interact with a SQL database.
    Given an input question '{input}', create a syntactically correct {dialect} query to run,
    then put the results only in the Answer field.

    Do not change the user's input question in any way.

    When sampling data, limit your results to {top_k} rows.

    Do not run any DML commands like INSERT, UPDATE, DELETE, or DROP.
    Only use SELECT statements.

    ...
    {tools}

    Use the following format:

    Question: the unchanged input question you must answer from the user
    Thought: reasoning about which tables/columns to query based on the question
    Action: the action to take, must be one of [{tool_names}]
    Action Input: input to the action
    Observation: the result of the action
    ... (this Thought/Action/Observation can repeat N times)
    Thought: I now know the final answer
    Answer: Final answer only. You must always return valid JSON fenced by a markdown code block. Do not return any additional text.

    {agent_scratchpad}
    """,
    input_variables=["input", "dialect", "top_k", "tool_names", "tools", "agent_scratchpad"]
)

agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    prompt=sql_agent_prompt,
    verbose=True,
    return_only_outputs=True,
    handle_parsing_errors=True
)

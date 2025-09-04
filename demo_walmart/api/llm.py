from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool, InfoSQLDatabaseTool, ListSQLDatabaseTool
from langchain.agents import AgentExecutor, create_sql_agent
from langchain.agents.agent_types import AgentType
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
    then put the results only in the Answer field.Unless the user specifies in his question a
    specific number of examples they wish to obtain, always limit your query to
    at most {top_k} results. You can order the results by a relevant column to
    return the most interesting examples in the database.

    Do not run any DML commands like INSERT, UPDATE, DELETE, or DROP.
    Only use SELECT statements.

    Pay attention to use only the column names that you can see in the schema
    description. Be careful to not query for columns that do not exist. Also,
    pay attention to which column is in which table.
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
    Answer: Final answer only.

    {agent_scratchpad}
    """,
    input_variables=["input", "dialect", "top_k", "tool_names", "tools", "agent_scratchpad"]
)

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10,
    return_only_outputs=True
)

agent = agent_executor
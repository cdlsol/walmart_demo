from langchain.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.agents import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
from db import engine
from langchain.prompts import PromptTemplate
from langchain.chains import create_sql_query_chain

load_dotenv()

db = SQLDatabase(engine)
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

sql_agent_prompt = PromptTemplate(
    template="""
    You are an agent designed to interact with a SQL database.
    Given an input question '{input}', create a syntactically correct {dialect} query to run,
    then put the results only in the Answer field. Unless the user specifies in his question a
    specific number of examples they wish to obtain, always limit your query to
    at most {top_k} results. You can order the results by a relevant column to
    return the most interesting examples in the database.

    You can check the database schema for available tables and columns and you can also
    check the semantic layer: {semantic_layer} for more information about the data and how to calculate certain metrics.
    If you cannot find the information you need in the semantic layer for a specific metric based on a
    column, then you can use the column directly.  

    Do not run any DML commands like INSERT, UPDATE, DELETE, or DROP.
    Only use SELECT statements.

    Only return SQL Query not anything else like ```sql ... ```
    NEVER wrap SQL queries in markdown fences such as ```sql or ```.
    ALWAYS output raw SQL only inside Action Input.
    If you include markdown syntax, the query will fail.

    Pay attention to use only the column names that you can see in the schema
    description. Be careful to not query for columns that do not exist. Also,
    pay attention to which column is in which table.
    ...
    {tools}

    Use the following format:

    Question: the unchanged input question you must answer from the user
    Thought: reasoning about which tables/columns to query based on the question
    Action: the action to take, must be one of [{tool_names}]
    Action Input: input to the action, if making a query, NEVER wrap SQL queries in markdown fences such as ```sql or ```
    Observation: the result of the action
    ... (this Thought/Action/Observation can repeat N times)
    if you have obtained an error in your Observation like "Error: (psycopg2.errors.SyntaxError) syntax error at or near "```" "
    then you must correct your SQL query by making sure you dont repeat the error log and try again.
    Thought: I now know the final answer
    Answer: Answer: Provide ONLY the final answer. Start your response with 'Answer:' and nothing else. Provide ONLY the final answer. Do not include bullets or newlines.

    {agent_scratchpad}
    """,
    input_variables=["input", "dialect", "top_k", "tool_names", "tools", "agent_scratchpad", "semantic_layer"]
)

sql_prompt = PromptTemplate(
    input_variables=["input", "top_k", "table_info"],
    template="""
    Given an input question '{input}', create a syntactically correct {dialect} query to run,
    then put the results only in the Answer field. Unless the user specifies in his question a
    specific number of examples they wish to obtain, always limit your query to
    at most {top_k} results. You can order the results by a relevant column to
    return the most interesting examples in the database.

    Rules:
    - Only return the SQL query, no explanation, no markdown.
    - Unless specified otherwise, limit to at most {top_k} results.
    - Only use the following tables: {table_info}.

    Question: {input}
    SQL Query:
    """
)

# Build Agent
# agent_executor = create_sql_agent(
#     llm=llm,
#     toolkit=toolkit,
#     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True,
#     handle_parsing_errors=True,
#     max_iterations=25,
#     return_only_outputs=True
# )
# agent = agent_executor

# Build the chain
write_query = create_sql_query_chain(
    llm=llm,
    db=db,
    prompt=sql_prompt,
    k=10  # top_k default
)
chain = write_query
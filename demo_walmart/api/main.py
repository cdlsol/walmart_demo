from fastapi import FastAPI
import logging
from llm import agent
from langchain.output_parsers import StructuredOutputParser
from pydantic import BaseModel
from dotenv import load_dotenv
import sys
import json

load_dotenv()

logger = logging.getLogger("api_logger")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.handlers[:] = [handler]   # replace any existing handlers

# with open("static/catalog.json") as f:
#     catalog = f.read()
# Escape curly braces so PromptTemplate doesn't interpret them
# catalog_escaped = catalog.replace("{", "{{").replace("}", "}}")

app = FastAPI()

@app.get("/health")
def health_check():
    logger.info("Health check endpoint called")
    return {"status": "ok"}

class QuestionRequest(BaseModel):
    question: str
@app.post("/question")
def question_endpoint(request: QuestionRequest):
    question = request.question
    try:
        logger.info(f"Received question: {question}")
        response = agent.invoke({
            "input": question,
            # "catalog": catalog_escaped,
            "tool_names": "sql_db",
            "dialect": "postgresql",
            "agent_scratchpad": "",
            "top_k": 10
        })
        try:
            answer = response["output"]
            # answer_json = json.loads(response["Answer"])
        except json.JSONDecodeError:
            answer_json = {"raw": response}
        return answer
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return {"error": str(e)}
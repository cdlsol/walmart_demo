from fastapi import FastAPI
import logging
from llm import agent
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("api_logger")
logging.basicConfig(filename='api.log', level=logging.INFO)

with open("static/catalog.json") as f:
    catalog = f.read()

# Escape curly braces so PromptTemplate doesn't interpret them
catalog_escaped = catalog.replace("{", "{{").replace("}", "}}")

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
            "catalog": catalog_escaped,
            "dialect": "postgresql",
            "top_k": 10
        })
        response_text = response.get("output_text", str(response))
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return {"error": str(e)}
    return {"answer": response_text}
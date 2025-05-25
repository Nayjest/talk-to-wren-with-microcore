import logging
import os

import requests

from mcp.server.fastmcp import FastMCP


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
mcp = FastMCP(name="WrenMCP", debug=True)
base_url = "https://cloud.getwren.ai/api/v1"
api_key = os.getenv("WREN_API_KEY")
project_id = os.getenv("WREN_PROJECT_ID")
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {api_key}"
}


@mcp.tool(description="Converts a natural language question into a SQL query")
def generate_sql(question: str) -> str:
    logging.info(f"Generating SQL for question: {question}")
    payload = {
        "question": question,
        "projectId": project_id,
    }
    response = requests.post(f"{base_url}/generate_sql", json=payload, headers=headers)
    result = response.json()
    logging.info(f"Result of generating SQL: {result}")
    return result["sql"]


@mcp.tool(description="Runs a SQL query and returns the results as structured data")
def run_sql(sql: str) -> str:
    payload = {
        "sql": sql,
        "projectId": project_id,
        "limit": 1000,
    }
    response = requests.post(f"{base_url}/run_sql", json=payload, headers=headers)
    result = response.json()
    logging.info(f"Result of running SQL: {result}")
    return result["records"]


@mcp.tool(description="Answer user question using Wren")
def answer_question(question: str) -> dict:
    try:
        sql = generate_sql(question)
        data = run_sql(sql)
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"error": str(e)}
    return dict(data=data, sql=sql)

mcp.run(transport="streamable-http")
# Intentionally leftover debug code
# res = generate_sql("What is qty of customers?")
# print(res)
# data = run_sql(res)
# print(data)
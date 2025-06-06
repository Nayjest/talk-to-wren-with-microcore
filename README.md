# Talk to your Database using Wren AI Service and AI-Microcore python library

This is example of minimalistic 16-line LLM-agnostic integration of the "Talk to your data" 
solution (Wren) into a custom agent using
[ai-microcore](https://github.com/Nayjest/ai-microcore).

## Source Code
```python
import asyncio, logging, microcore as mc
async def main():
    logging.basicConfig(level=logging.INFO)
    mc.configure(USE_LOGGING=True, MCP_SERVERS=[{"name": "wren", "url": "ws://localhost:8000/mcp/"}])
    mcp = await mc.mcp_server("wren").connect()
    messages = [mc.prompt("""
        [Task]
        Answer following question using tools: {{question}}
        [Tools]
        {{tools}}
        """, question=input("Ask your data: "), tools=mcp.tools, remove_indent=True
    ).as_system]
    while (llm_answer := mc.llm(messages)).is_tool_call():
        messages += [llm_answer.as_assistant, await mcp.exec(llm_answer)]
    print("The final answer is:\n", mc.ui.magenta(llm_answer))
asyncio.run(main())
```

## Output
```
PS C:\CODE\mcp-exp> python app.py
INFO:Connecting to MCP ws://localhost:8000/mcp/...
INFO:mcp.client.streamable_http:Connecting to StreamableHTTP endpoint: ws://localhost:8000/mcp/
INFO:Initializing MCP session (ws://localhost:8000/mcp/)
INFO:HTTP Request: POST ws://localhost:8000/mcp/ "HTTP/1.1 200 OK"
INFO:mcp.client.streamable_http:Received session ID: adca71fdb74046f89aa3828582d4f111
INFO:Checking MCP tools cache for ws://localhost:8000/mcp/...
INFO:Using MCP tools from cache for ws://localhost:8000/mcp/
Ask your data: What is qty of customers
Requesting LLM gpt-4.1:
    [System]:
        [Task]
        Answer following question using tools: What is qty of customers
        [Tools]
        # Converts a natural language question into a SQL query
        {
          "call": "generate_sql",
          "question": <string> Question
        }
        # Runs a SQL query and returns the results as structured data
        {
          "call": "run_sql",
          "sql": <string> Sql
        }
        # Answer user question using Wren
        {
          "call": "answer_question",
          "question": <string> Question
        }

INFO:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
LLM Response:
    {
      "call": "generate_sql",
      "question": "What is the quantity of customers?"
    }
INFO:Calling MCP tool generate_sql with {'question': 'What is the quantity of customers?'}...
INFO:HTTP Request: GET ws://localhost:8000/mcp/ "HTTP/1.1 200 OK"
INFO:HTTP Request: POST ws://localhost:8000/mcp/ "HTTP/1.1 202 Accepted"
INFO:HTTP Request: POST ws://localhost:8000/mcp/ "HTTP/1.1 200 OK"
Requesting LLM gpt-4.1:
    [System]:
        [Task]
        Answer following question using tools: What is qty of customers
        [Tools]
        # Converts a natural language question into a SQL query
        {
          "call": "generate_sql",
          "question": <string> Question
        }
        # Runs a SQL query and returns the results as structured data
        {
          "call": "run_sql",
          "sql": <string> Sql
        }
        # Answer user question using Wren
        {
          "call": "answer_question",
          "question": <string> Question
        }
    [Assistant]:
        {
          "call": "generate_sql",
          "question": "What is the quantity of customers?"
        }
    [User]:
        SELECT count(*) as qty FROM customers

INFO:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
LLM Response:
    {
      "call": "run_sql",
      "sql": "SELECT count(*) as qty FROM customers"
    }
INFO:Calling MCP tool run_sql with {'sql': 'SELECT count(*) as qty FROM customers'}...
INFO:HTTP Request: POST ws://localhost:8000/mcp/ "HTTP/1.1 200 OK"
Requesting LLM gpt-4.1:
    [System]:
        [Task]
        Answer following question using tools: What is qty of customers
        [Tools]
        # Converts a natural language question into a SQL query
        {
          "call": "generate_sql",
          "question": <string> Question
        }
        # Runs a SQL query and returns the results as structured data
        {
          "call": "run_sql",
          "sql": <string> Sql
        }
        # Answer user question using Wren
        {
          "call": "answer_question",
          "question": <string> Question
        }
    [Assistant]:
        {
          "call": "generate_sql",
          "question": "What is the quantity of customers?"
        }
    [User]:
        SELECT count(*) as qty FROM customers
    [Assistant]:
        {
          "call": "run_sql",
          "sql": "SELECT count(*) as qty FROM customers"
        }
    [User]:
        {
          "qty": 77
        }  

INFO:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
LLM Response:
    The quantity of customers is 77.

The final answer is:
 The quantity of customers is 77.
```

## Running custom MCP server from this repo:
```bash
python wren_mcp.py
```
Code expects following ENV variables:
- WREN_API_KEY
- WREN_PROJECT_ID

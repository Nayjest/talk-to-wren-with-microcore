# Talk to your Database agent using Wren & AI-Microcore

This script [app.py](app.py) demonstrates minimalistic 16-line LLM-agnostic integration of the "Talk to your data" 
solution (Wren) into a custom agent using
[ai-microcore](https://github.com/Nayjest/ai-microcore).

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
    while (llm_answer := mc.llm(messages)).contains_valid_json():
        messages += [llm_answer.as_assistant, await mcp.exec(llm_answer)]
    print("The final answer is:\n", mc.ui.magenta(llm_answer))
asyncio.run(main())
```
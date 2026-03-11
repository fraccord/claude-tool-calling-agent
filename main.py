import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Definisi tool sederhana: calculator
tools = [
    {
        "name": "calculator",
        "description": "Perform basic arithmetic calculations safely. Input is a math expression like '2 + 3 * 4'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate (e.g., '15 * (8 + 7)')."
                }
            },
            "required": ["expression"]
        }
    }
]

def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "calculator":
        expr = tool_input.get("expression")
        if not expr:
            return "Error: No expression provided."
        
        # Safe eval: batasi globals/locals
        try:
            # Hanya izinkan operasi math dasar
            result = eval(
                expr,
                {"__builtins__": {}},
                {"__builtins__": {}, "abs": abs, "pow": pow, "round": round}
            )
            return str(result)
        except Exception as e:
            return f"Error evaluating expression: {str(e)}"
    
    return f"Unknown tool: {tool_name}"

def run_agent_loop(user_query: str, max_turns: int = 5):
    messages = [{"role": "user", "content": user_query}]
    
    for turn in range(max_turns):
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",  # atau model lain yang support tool use
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Cek apakah ada tool_use di response
        tool_use_block = None
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_use_block = content_block
                break
        
        if not tool_use_block:
            # No tool needed → final answer
            final_text = ""
            for block in response.content:
                if block.type == "text":
                    final_text += block.text
            return final_text.strip()
        
        # Ada tool_use → execute tool
        tool_name = tool_use_block.name
        tool_input = tool_use_block.input
        
        tool_result = execute_tool(tool_name, tool_input)
        
        # Tambah tool_use dan tool_result ke history
        messages.append({
            "role": "assistant",
            "content": [{"type": "tool_use", **tool_use_block.model_dump()}]
        })
        messages.append({
            "role": "user",
            "content": [{
                "type": "tool_result",
                "tool_use_id": tool_use_block.id,
                "content": tool_result
            }]
        })
    
    return "Max turns reached. Last response: " + response.content[0].text

# Jalankan dari terminal
if __name__ == "__main__":
    print("Claude Tool-Calling Agent Demo")
    print("Ketik 'exit' untuk keluar.\n")
    
    while True:
        query = input("You: ").strip()
        if query.lower() in ["exit", "quit", "q"]:
            break
        if not query:
            continue
        
        print("\nAgent thinking...\n")
        answer = run_agent_loop(query)
        print("Agent:", answer, "\n")

import json

from groq import Groq

from config import (
    GROQ_API_KEY,
    MODEL,
    MAX_ITERATIONS
)

from prompts import SYSTEM_PROMPT

from tools import AVAILABLE_FUNCTIONS


# =========================================================
# Validate API Key
# =========================================================

if not GROQ_API_KEY:

    raise RuntimeError(
        "GROQ_API_KEY is missing. "
        "Please add it to your .env file."
    )


# =========================================================
# Groq Client
# =========================================================

client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# Tool Schemas
# =========================================================

TOOLS = [

    {
        "type": "function",

        "function": {

            "name": "calculator",

            "description": (
                "Perform mathematical calculations. "
                "Use this tool when the user asks "
                "for arithmetic or numerical calculations."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "expression": {

                        "type": "string",

                        "description": (
                            "A mathematical expression. "
                            "Example: 25 * 4 + 10"
                        )
                    }
                },

                "required": [
                    "expression"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "read_file",

            "description": (
                "Read a local research text file "
                "from the data folder."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "filename": {

                        "type": "string",

                        "description": (
                            "Name of the text file "
                            "inside the data folder."
                        )
                    }
                },

                "required": [
                    "filename"
                ]
            }
        }
    },

    {
        "type": "function",

        "function": {

            "name": "search",

            "description": (
                "Search for research information. "
                "Use this when the user asks to "
                "research or search for a topic."
            ),

            "parameters": {

                "type": "object",

                "properties": {

                    "query": {

                        "type": "string",

                        "description": (
                            "The research topic "
                            "or search query."
                        )
                    }
                },

                "required": [
                    "query"
                ]
            }
        }
    }
]


# =========================================================
# Tool Execution
# =========================================================

def execute_tool(tool_call):

    try:

        function_name = (
            tool_call.function.name
        )

        print(
            f"\n[Tool Selected] "
            f"{function_name}"
        )

        # Validate tool name
        if function_name not in AVAILABLE_FUNCTIONS:

            return {
                "success": False,
                "error": (
                    f"Unknown tool: "
                    f"{function_name}"
                )
            }

        # Parse arguments
        try:

            arguments = json.loads(
                tool_call.function.arguments
            )

        except json.JSONDecodeError:

            return {
                "success": False,
                "error": (
                    "Tool arguments "
                    "were not valid JSON."
                )
            }

        # Get Python function
        function = AVAILABLE_FUNCTIONS[
            function_name
        ]

        # Execute
        result = function(
            **arguments
        )

        print(
            f"[Tool Result] {result}"
        )

        return result

    except Exception as e:

        return {
            "success": False,
            "error": (
                f"Tool execution failed: "
                f"{str(e)}"
            )
        }


# =========================================================
# Agent
# =========================================================

def run_agent(user_question):

    messages = [

        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },

        {
            "role": "user",
            "content": user_question
        }
    ]

    # =====================================================
    # Agent Loop
    # =====================================================

    for iteration in range(
        MAX_ITERATIONS
    ):

        print(
            f"\n========== "
            f"Iteration {iteration + 1}"
            f" =========="
        )

        print(
            "[Agent] Thinking..."
        )

        try:

            response = (
                client.chat.completions.create(

                    model=MODEL,

                    messages=messages,

                    tools=TOOLS,

                    tool_choice="auto",

                    temperature=0.2,

                    max_completion_tokens=2048
                )
            )

        except Exception as e:

            return (
                "I could not contact the "
                "LLM service.\n\n"
                f"Error: {str(e)}"
            )

        message = (
            response.choices[0].message
        )

        # =================================================
        # No Tool Call
        # =================================================

        if not message.tool_calls:

            print(
                "[Agent] No more tools needed."
            )

            return (
                message.content
                or "No response was generated."
            )

        # =================================================
        # Add Assistant Tool Call
        # =================================================

        messages.append(message)

        # =================================================
        # Execute All Tool Calls
        # =================================================

        for tool_call in message.tool_calls:

            result = execute_tool(
                tool_call
            )

            # Add tool result
            messages.append(

                {
                    "role": "tool",

                    "tool_call_id":
                        tool_call.id,

                    "name":
                        tool_call.function.name,

                    "content":
                        json.dumps(
                            result,
                            ensure_ascii=False
                        )
                }
            )

    # =====================================================
    # Maximum Iterations Reached
    # =====================================================

    return (
        "The agent stopped because "
        f"it reached the maximum limit "
        f"of {MAX_ITERATIONS} iterations."
    )
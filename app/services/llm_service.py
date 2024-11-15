from connections.chatgpt import ChatGPTConnection
import json


class LLMService:
    def __init__(self, chatgpt_conn: ChatGPTConnection):
        self.chatgpt_conn = chatgpt_conn

    async def split_task(self, title: str, description: str, n: int = 2) -> list:
        """
        Use ChatGPT to split a task into 'n' subtasks (default 2) and return a list of subtasks as objects.
        """
        # Generate a prompt to ask ChatGPT to return a well-structured JSON response with 'n' subtasks
        prompt = (
            f"Split the following task into {n} subtasks in the form of a JSON object:\n"
            f"Title: {title}\nDescription: {description}\n"
            f"The response should be a JSON array of {n} objects, where each object has the following format:\n"
            "[\n"
            "  {\n"
            '    "title": "Subtask Title",\n'
            '    "description": "Subtask Description"\n'
            "  },\n"
            "  ...\n"
            "  {\n"
            '    "title": "Subtask Title",\n'
            '    "description": "Subtask Description"\n'
            "  }\n"
            "]\n"
            "Make sure the titles and descriptions are clear and concise."
        )

        # Ask ChatGPT to process the prompt and return a structured JSON response

        # Try to parse the response as JSON

        subtasks = await self.chatgpt_conn.ask_gpt(prompt)

        # Ensure the response contains exactly 'n' subtasks
        if len(subtasks) != n:
            raise ValueError(
                f"ChatGPT did not return exactly {n} subtasks in the JSON response."
            )

        # Validate each subtask contains both 'title' and 'description'
        for subtask in subtasks:
            if (
                not isinstance(subtask, dict)
                or "title" not in subtask
                or "description" not in subtask
            ):
                raise ValueError(
                    "Each subtask must contain both 'title' and 'description' keys."
                )

        return subtasks

from openai import AsyncOpenAI

import re
import json


class ChatGPTConnection:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.aclient = AsyncOpenAI(api_key=self.api_key)

    async def ask_gpt(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> dict:
        """
        Send a prompt to ChatGPT and get a response in well-formed JSON.
        """
        try:
            # Add a system prompt to ensure that the response is well-formed JSON
            system_prompt = (
                "Return all responses as valid, well-formed JSON. "
                "Ensure the JSON structure is correct, and if you are generating a list or object, "
                "use the appropriate format. Do not return code blocks or other text formats, just the raw JSON."
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ]

            # Make the API request to generate text asynchronously
            completion = await self.aclient.chat.completions.create(
                model="gpt-4o",  # Ensure this model is available for your use
                messages=messages,
                max_tokens=3000,
                temperature=0.7,
            )

            # Extract and return the generated text
            generated_text = completion.choices[0].message.content

            # Strip the code block markers if they exist
            cleaned_response = self._strip_code_block_markers(generated_text)

            # Parse the cleaned response into a JSON object
            return json.loads(cleaned_response)

        except Exception as e:
            # Log the exception as needed and raise an error
            raise RuntimeError(f"ChatGPT query failed: {str(e)}")

    def _strip_code_block_markers(self, response: str) -> str:
        """
        Strip the '```json' and '```' code block markers from the response.
        """
        # Remove the leading and trailing code block markers (if they exist)
        response = re.sub(r"^```json\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

        return response.strip()

import os
import json
import re
from mistralai import Mistral


class MistralConnection:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = Mistral(api_key=self.api_key)

    async def ask_mistral(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> dict:
        """
        Send a prompt to Mistral and get a response in well-formed JSON.
        """
        try:
            # Prepare the messages for the Mistral chat API
            messages = [{"role": "user", "content": prompt}]

            # Make the API request to generate text asynchronously
            chat_response = await self.client.chat.complete_async(
                model="mistral-large-latest", messages=messages  # The model to use
            )

            # Print the response to check its structure
            print(chat_response)  # Add this line to inspect the response structure

            # Assuming chat_response is an object with attributes, access them accordingly:
            # (This is a guess, you'll need to adjust according to actual structure)
            if hasattr(chat_response, "choices") and len(chat_response.choices) > 0:
                generated_text = chat_response.choices[0].message.content
            else:
                raise ValueError("Invalid response structure or no choices returned")

            # Return the response as JSON (already a string, no need to parse again)
            return self._strip_code_block_markers(generated_text)

        except Exception as e:
            # Log the exception and raise a runtime error
            raise RuntimeError(f"Mistral query failed: {str(e)}")

    def _strip_code_block_markers(self, response: str) -> str:
        """
        Strip the '```json' and '```' code block markers from the response.
        """
        # Remove the leading and trailing code block markers (if they exist)
        response = re.sub(r"^```json\s*", "", response)
        response = re.sub(r"\s*```$", "", response)

        return response.strip()

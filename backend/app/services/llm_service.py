from connections.mistral import MistralConnection  # Updated import to Mistral


class LLMService:
    def __init__(self, mistral_conn: MistralConnection):
        self.mistral_conn = mistral_conn

    async def ask_mistral(self, prompt: str) -> str:
        """
        Call Mistral API with the provided prompt and return the response as a string.
        """
        return await self.mistral_conn.ask_mistral(prompt)

import requests
import subprocess

# STUPID THINGS
DEFAULT_PROMPT = """A close up face of a man staring in to the eyes of the viewer intensly.
The man's face is covered in wrinkles. A tattoo on forehead with text 'PROMPT MISSING'.
He has beautiful wavy long hair and big blue eyes.
"""
PROMPT_TEMPLATE = """You are an artist AI that accepts a text description and responds with same description with additional visual details in natural language.
Description: {}
Detailed Description:"""


class SmartPrompt:
    model_list = []

    try:
        model_list = requests.get("http://localhost:1234/api/v0/models").json()["data"]
    except:
        model_list = []

    def __init__(self) -> None:
        pass

    def enhance_with_llm(
        self, prompt: str, model: str, seed: int, provider: str = "LM Studio"
    ):
        response = requests.post(
            "http://localhost:1234/api/v0/completions",
            headers={"Content-Type": "application/json"},
            json={
                "model": model,
                "ttl": 0,
                "prompt": PROMPT_TEMPLATE.format(prompt),
                "temparature": 0.7,
                "max_tokens": 512,
                "stream": False,
                "seed": seed,
                "stop": "\n",
            },
        ).json()

        enhanced_prompt = response["choices"][0]["text"].strip()
        return enhanced_prompt

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "prompt": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": s.model_list[0]["id"]
                        if s.model_list
                        else "None available",
                    },
                ),
                "provider": (["LM Studio"], {}),
                "model": ([model["id"] for model in s.model_list], {}),
            },
            "optional": {
                "seed": ("INT", {"default": 0}),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "expand_prompt"

    @classmethod
    def IS_CHANGED(s, prompt: str, provider: str, model: dict, seed: int):
        return {prompt, provider, model, seed}.__dict__

    def expand_prompt(
        self, prompt: str, provider: str, model: dict, seed: int
    ) -> tuple[str]:
        prompt = self.enhance_with_llm(
            prompt,
            model,
            seed,
            provider,
        )
        subprocess.run([f"lms unload {model}"], shell=True)
        return (prompt,)

    OUTPUT_NODE = False

    CATEGORY = "HandyUtils"


NODE_CLASS_MAPPINGS = {
    "SmartPrompt": SmartPrompt,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SmartPrompt": "Smart Prompt",
}

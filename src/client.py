import requests
import json
from collections.abc import Generator

# LM Studio API Endpoint
API_URL = "http://localhost:1234/v1/chat/completions"

def get_completion(prompt: str, history: list) -> Generator[str, None, None]:
    """
    Sends a request to the LM Studio API with the given prompt and conversation history,
    and yields the model's response tokens as a stream.

    :param prompt: The user's new input.
    :param history: The previous conversation history (list of message objects).
    :return: A generator that yields the response tokens.
    """
    headers = {"Content-Type": "application/json"}

    # Add the new user prompt to the history
    messages = history + [{"role": "user", "content": prompt}]

    payload = {
        "model": "gpt-oss-120b",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": -1,  # Unlimited
        "stream": True  # Enable streaming
    }

    try:
        # The stream=True parameter is crucial for handling streaming responses
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), stream=True)
        response.raise_for_status()  # Raise an exception for non-2xx status codes

        for line in response.iter_lines():
            if line:
                # SSE lines are expected to start with "data: "
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    json_str = line_str[len('data: '):]
                    if json_str.strip() == '[DONE]':
                        break
                    try:
                        chunk = json.loads(json_str)
                        if "choices" in chunk and len(chunk["choices"]) > 0:
                            delta = chunk["choices"][0].get("delta", {})
                            token = delta.get("content")
                            if token:
                                yield token
                    except json.JSONDecodeError:
                        print(f"Error: Could not decode JSON from stream: {json_str}")
                        continue

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

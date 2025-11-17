from src.client import get_completion
import sys

def main():
    """
    Runs the main conversation loop.
    """
    # List to store the conversation history
    conversation_history = []

    print("Welcome! Starting a conversation with LM Studio.")
    print("Type 'exit' or 'quit' to end the program.")
    print("-" * 30)

    while True:
        try:
            # Get user input
            user_prompt = input("> ")

            # Check for exit commands
            if user_prompt.lower() in ["exit", "quit"]:
                print("Exiting the program.")
                break

            # Call the API to get the streaming response
            response_generator = get_completion(user_prompt, conversation_history)

            full_response = ""
            print("\nAssistant: ", end="")
            for token in response_generator:
                # Print each token as it arrives
                print(token, end="", flush=True)
                full_response += token
            
            # Print a newline after the response is complete
            print("\n")

            if full_response:
                # Add user input and the full model response to the history
                conversation_history.append({"role": "user", "content": user_prompt})
                conversation_history.append({"role": "assistant", "content": full_response})
            else:
                print("Did not receive a response from the model. Please try again.")

        except KeyboardInterrupt:
            print("\nProgram interrupted. Exiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion

def main():
    # Initialize the kernel
    kernel = Kernel()

    # Configure AI service
    api_key = "your-api-key-here"  # Replace with your actual OpenAI API key
    model = "gpt-3.5-turbo"  # Or another model of your choice

    # Add OpenAI chat completion service to the kernel
    kernel.add_service(
        OpenAIChatCompletion(service_id="chat-gpt", ai_model_id=model, api_key=api_key)
    )

    # Define a simple function that uses Semantic Kernel
    @kernel_function()
    def greet(name: str) -> str:
        template = "Hello, {{$name}}! Welcome to Semantic Kernel."
        return kernel.create_semantic_function(template, max_tokens=200)

    # Use the function
    greeting_function = greet()
    result = kernel.invoke(greeting_function, name="World")

    print(result)

if __name__ == "__main__":
    main()
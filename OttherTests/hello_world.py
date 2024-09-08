import os
from dotenv import load_dotenv
from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Initialize the kernel
    kernel = Kernel()

    # Get configuration from environment variables
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

    if not all([api_key, deployment_name, endpoint]):
        raise ValueError("Missing required Azure OpenAI configuration in .env file")

    # Add Azure OpenAI chat completion service to the kernel
    chat_service = AzureChatCompletion(
        service_id="azure-chat",
        deployment_name=deployment_name,
        endpoint=endpoint,
        api_key=api_key
    )
    kernel.add_service(chat_service)

    # Define a simple function that uses Semantic Kernel
    @kernel_function(description="Greet a person")
    def greet(context, name: str) -> str:
        template = f"Hello, {name}! Welcome to Semantic Kernel with Azure OpenAI."
        return template

    # Register the function with the kernel
    kernel.add_function(greet)

    # Use the function
    result = kernel.invoke("greet", name="World")

    print(result)

    # Example of using the AI service
    chat_function = kernel.create_semantic_function("Tell me a short joke about {{$input}}")
    joke_result = kernel.invoke(chat_function, input="programming")
    print(f"\nHere's a joke about programming:\n{joke_result}")

if __name__ == "__main__":
    main()
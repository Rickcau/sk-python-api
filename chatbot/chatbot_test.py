import asyncio
import os
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings, AzureChatCompletion

# This is a simple chatbot that uses the Semantic Kernel and Azure OpenAI to provide responses to user input
# it's intended to be run in a local environment, but you can adapt it to run in a serverless function
# the goal is to keep everything very simple and it help you understand the options for how to assoicate the chatbot with the Azure OpenAI service endpoints and API keys

async def get_chatbot_response(user_input: str) -> str:
    try:
        # Initialize chat history
        chat_history = ChatHistory()
        kernel = Kernel()
        service_id = "chatbot_service"
        
        # Use environment variables for sensitive information
        # here is one example of adding the AzureChatCompletion service to the kernel
        # api_key=os.environ.get("AZURE_OPENAI_API_KEY")
        # endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT") 
        # deployment_name=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME") 
        api_key="<add your key here>"
        endpoint="<add your endpoint here>"
        deployment_name="<add your deployment name here>" 
        
        kernel.add_service(AzureChatCompletion(
            service_id=service_id,
            api_key=api_key,
            endpoint=endpoint,
            deployment_name=deployment_name,
        ))
        
        # Here is another example of adding the AzureChatCompletion service to the kernel
        # By default, the service uses the environment variables for the API key, endpoint, and deployment name found in the .env file
        # take a look at the .env.example file for an example of how to set these variables
        # kernel.add_service(AzureChatCompletion(
        #     service_id="gpt-4o"
        # ))
        
        chat_history.add_system_message("You are a helpful assistant.")
        
        # Define the prompt template configuration
        template = """
        Previous information from chat:
        {{$chat_history}}
        
        User: {{$request}}
        Assistant:
        """
        
        prompt_template_config = PromptTemplateConfig(
            template=template,
            name="chat",
            description="Chat with the assistant",
            template_format="semantic-kernel",
            input_variables=[
                InputVariable(name="chat_history", description="The conversation history", is_required=False, default=""),
                InputVariable(name="request", description="The user's request", is_required=True),
            ],
            execution_settings=OpenAIChatPromptExecutionSettings(service_id=service_id, max_tokens=4000, temperature=0.2),
        )
  
        # OpenAIChatPromptExecutionSettings(service_id=service_id, max_tokens=4000, temperature=0.2)
        
        # Add the function to the kernel
        chat_function = kernel.add_function(
            function_name="chat",
            plugin_name="ChatBot",
            prompt_template_config=prompt_template_config,
        )
        
        # Invoke the chat function with user input and chat history
        answer = await kernel.invoke(
            function=chat_function,
            arguments=KernelArguments(
                request=user_input,
                chat_history=str(chat_history),  # Convert chat history to string
            ),
        )
        
        chat_history.add_user_message(user_input)
        chat_history.add_assistant_message(str(answer))
        
        # Return the answer from the assistant
        return str(answer)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, but I encountered an error while processing your request."

# async def main():
#     print("Chatbot initialized. Type 'quit' to exit.")
    
#     while True:
#         user_input = input("You: ")
#         if user_input.lower() == 'quit':
#             print("Goodbye!")
#             break
        
#         response = await get_chatbot_response(user_input)
#         print(f"Assistant: {response}")

# if __name__ == "__main__":
#     asyncio.run(main())
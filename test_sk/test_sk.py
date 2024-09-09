import os
import asyncio
import sys
from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings, AzureChatCompletion
from semantic_kernel.functions import kernel_function


async def test_sk(user_input: str) -> str:
    try:
        kernel = Kernel()
        api_key="<add your key here>"
        endpoint="<add your endpoint here>"
        deployment_name="<add your deployment name here>" 
        
        chat_history = ChatHistory(
            system_message="When responding to the user's request be nice and helpful. "
        ) 
        
        # Add Azure OpenAI chat completion service to the kernel
        chat_service = AzureChatCompletion(
            service_id="azure-chat",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key
        )
        kernel.add_service(chat_service)
        # Register the function with the kernel
        
        chat_function = kernel.add_function(
            plugin_name="ChatBot",
            function_name="Chat",
            prompt="{{$chat_history}}{{$user_input}}",
            template_format="semantic-kernel",
        )
        settings = kernel.get_prompt_execution_settings_from_service_id(service_id="azure-chat")
        settings.max_tokens = 2000
        settings.temperature = 0.7
        settings.top_p = 0.8
        answer = await kernel.invoke(
            chat_function, KernelArguments(settings=settings, user_input=user_input, chat_history=chat_history)
        )
        return answer 
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, but I encountered an error while processing your request."

async def main():
    print("Running the Test_sk.py code.")    
    response = await test_sk("Why is the sky blue?")
    print(f"Assistant: {response}")

async def run_async_main():
    try:
        await main()
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught. Exiting gracefully.")
    except Exception as e:
        print("An error occurred: %s", str(e))

if __name__ == "__main__":
    if sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(run_async_main())
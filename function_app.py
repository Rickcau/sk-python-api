import os
import asyncio
import azure.functions as func
import logging
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorLogExporter,
    AzureMonitorTraceExporter)

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.trace import set_tracer_provider
from opentelemetry.sdk.resources import Resource
# from chatbot_test import get_chatbot_response

from semantic_kernel import Kernel
from semantic_kernel.functions import KernelArguments
from semantic_kernel.prompt_template import InputVariable, PromptTemplateConfig
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.connectors.ai.open_ai import OpenAIChatPromptExecutionSettings, AzureChatCompletion
from semantic_kernel.functions import kernel_function

logging.basicConfig(level=logging.DEBUG)


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
instrumentation_key = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")

# Create a resource to represent the service/sample
resource = Resource.create({ResourceAttributes.SERVICE_NAME: "TelemetryExample"})

def set_up_tracing():
    trace_exporter = AzureMonitorTraceExporter(connection_string=instrumentation_key )

    # Initialize a trace provider for the application. This is a factory for creating tracers.
    # tracer_provider = TracerProvider()
    tracer_provider = TracerProvider(resource=resource)
    # Span processors are initialized with an exporter which is responsible
    # for sending the telemetry data to a particular backend.
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    # Sets the global default tracer provider
    set_tracer_provider(tracer_provider)

set_up_tracing()
        
@app.route(route="http_trigger")
async def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        prompt = req_body.get('prompt')
              
        if prompt:
            
            # response = await get_chatbot_response(prompt)
            response = await test_sk(prompt)
            logging.info(f"Assistant: {response}")
            return func.HttpResponse(
                f"Response: {response}", 
                status_code=200
            )
        else:
            return func.HttpResponse(
                "Please provide a 'prompt' in the request body JSON.",
                status_code=400
            )
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON in the request body.",
            status_code=400
        )
        
async def test_sk(user_input: str) -> str:
    try:
        kernel = Kernel()
        # api_key="<add your key here>"
        # endpoint="<add your endpoint here>"
        # deployment_name="<add your deployment name here>" 
        api_key="xxx <yourAPI Key> 4f0d876d6e3ecb277d8b"
        endpoint="https://<your endpoint>.openai.azure.com/"
        deployment_name="gpt-4o" 
        chat_history = ChatHistory(
            system_message="When responding to the user's request be nice and helpful. "
        ) 
        
        # Add Azure OpenAI chat completion service to the kernel
        chat_service = AzureChatCompletion(
            service_id="azure-chat",
            deployment_name=deployment_name,
            endpoint=endpoint,
            api_key=api_key,
            api_version="2024-02-01"
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

    

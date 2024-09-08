import os
import azure.functions as func
import logging
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorLogExporter,
    AzureMonitorTraceExporter)

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider



app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
instrumentation_key = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")

def set_up_tracing():
    trace_exporter = AzureMonitorTraceExporter(connection_string=instrumentation_key )

    # Initialize a trace provider for the application. This is a factory for creating tracers.
    tracer_provider = TracerProvider()
    # Span processors are initialized with an exporter which is responsible
    # for sending the telemetry data to a particular backend.
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    # Sets the global default tracer provider
    set_tracer_provider(tracer_provider)
        
@app.route(route="http_trigger")
async def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        req_body = req.get_json()
        prompt = req_body.get('prompt')
        set_up_tracing()
        
        if prompt:
            from chatbot.chatbot_test import get_chatbot_response
            response = await get_chatbot_response(prompt)
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
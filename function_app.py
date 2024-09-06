import os
import azure.functions as func
import logging
from azure.monitor.opentelemetry.exporter import (
    AzureMonitorLogExporter,
    AzureMonitorTraceExporter)

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import set_tracer_provider

import chatbot_test

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
instrumentation_key = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")

def set_up_tracing():
    trace_exporter = AzureMonitorTraceExporter(connection_string="InstrumentationKey=9ef3dff9-42aa-486c-828c-22e368e55809;IngestionEndpoint=https://eastus-8.in.applicationinsights.azure.com/;LiveEndpoint=https://eastus.livediagnostics.monitor.azure.com/;ApplicationId=15cd47dc-de26-4cf9-bb72-baf02592192d")

    # Initialize a trace provider for the application. This is a factory for creating tracers.
    tracer_provider = TracerProvider()
    # Span processors are initialized with an exporter which is responsible
    # for sending the telemetry data to a particular backend.
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    # Sets the global default tracer provider
    set_tracer_provider(tracer_provider)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
# sk-python-api

## test_sk.py
This file is for testing SK and make sure the calls are working before trying to use them from the Python Azure Function.

**How to run the test_sk.py outside of the Azure Function.
1. Open a new Terminal Window
2. CD test_sk
3. python test_sk

The SK will call the LLM with the prompt "Why is the Sky Blue?" and you will get a proper response in the terminal Window.

## How to reproduce the issue.
The test_sk() function has already been copied into the function_app.py file.

** Important Note **
You will need to change these values in the test_sk() function within the **function_app.py** file to point to your AI endpoint details.

   ~~~
      api_key="<add your key here>"
      endpoint="<add your endpoint here>"
      deployment_name="<add your deployment name here>" 
   ~~~

1. Open a new Terminal Window
2. Make sure you are located in the SK-Python-Api folder
3. run "function start function_app.py"
4. Open Bruno or Postman and make a POST request using the following URL http://localhost:7071/api/http_trigger
5. Pass as the request body the following JSON

   ~~~
       {
          "prompt": "Why is the sky blue?"
       }
   ~~~

-OR-

Run the following CURL command from the Terminal

   ~~~
         curl -X POST http://localhost:7071/api/http_trigger -H "Content-Type: application/json" -d "{\"prompt\": \"Why is the sky blue?\"}"
   ~~~

** Here is the error you will get when running the **test_sk()** function from within the **function_app.py**

`Error: Something went wrong in function invocation. During function invocation: 'ChatBot-Chat'. Error description: 'Error occurred while invoking function Chat: ("<class 'semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion.AzureChatCompletion'> service failed to complete the prompt", NotFoundError("Error code: 404 - {'error': {'code': '404', 'message': 'Resource not found'}}"))'`

** It's important to note that this never happens if running the test_sk.py directly! **
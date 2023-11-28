from openai import OpenAI
import time

import ifcopenshell
import ifcopenshell.geom
from datetime import datetime
import io
import contextlib

# Open the IFC file
#ifc_file = ifcopenshell.open("C:\\Users\\cdri\\Downloads\\23134_Buildwise_REVIT_vB\\23134_Buildwise_REVIT_vB.ifc")
ifc_file = ifcopenshell.open("C:\\Users\\cdri\\Downloads\\23134_Buildwise_REVIT_vB\\B4WArch.ifc")

#TestEnv
exec('print(dir())')
#EndTestEnv

client = OpenAI()

assistant_id = "asst_zes9q5sYVHyXmbdDnDuMdU9E" # Takes question from client, turns it into python code to run
assistant_id_output = "y" # Takes result from Python code from previous assistant and interprets it
user_input = input("Q: ")

def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)


def create_thread_and_run(user_input, assistant_id):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run


# Waiting in a loop
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

def process_bot_response(response):
    # Check if the response starts with 'TEXT'
    isText = False
    execution_result = "Error occurred"
    response.strip()
    #print(response)
    if response.startswith("TEXT"):
        # Print everything after 'TEXT'
        response = response[4:]
        execution_result = response  # 4 is the length of 'TEXT'
        isText = True
    elif response.startswith("```python") and response.endswith("```"):
        print("starts w python\n")
        response = response[9:-3]
        print(response)
    else:
        print("good code\n")
        print(response)
    if isText is False:
        # Redirect standard output to capture the execution result
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                exec(response, globals())
                # Get the output of the executed code
                execution_result = buf.getvalue().strip()
        except:
            print("Error: ", response)

    return execution_result, isText

# Running connection
thread1, run1 = create_thread_and_run(user_input, assistant_id)

while True:
    # Wait for Run 1
    run1 = wait_on_run(run1, thread1)
    response1 = get_response(thread1)
    response1_text = response1.data[0].content[0].text.value
    #print("\n", response1_text, "\n")
    execution_result, isText = process_bot_response(response1_text)
    print(execution_result, "\n")
    if isText:
        user_input = input("Q: ")
    else:
        user_input = "Exec result: " + execution_result
    print(user_input)
    run1 = submit_message(assistant_id, thread1, user_input)


# thread2, run2 = create_thread_and_run(execution_result,
#                                       assistant_id_output)
#
# # Wait for Run 2
# run2 = wait_on_run(run2, thread2)
# response2 = get_response(thread2)
# response2_text = response2.data[0].content[0].text.value
# print(response2_text)


# # CODE TO RUN response1_text HERE
# def safe_exec(code, context):
#     """
#     Safely execute the provided code string within a given context.
#     """
#     try:
#         with contextlib.redirect_stdout(io.StringIO()) as output:
#             exec(code, context)
#             return output.getvalue()
#     except Exception as e:
#         return str(e)
#
# # Define a context for the execution
# execution_context = {
#     'ifcopenshell': ifcopenshell,
#     'ifc_file': ifc_file,
#     # Add other allowed functions or objects here
# }
#
# # Execute the response1_text
# execution_result = safe_exec(response1_text, execution_context)
# print("Execution Result:", execution_result)
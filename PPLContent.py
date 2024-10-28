import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import jsonschema

from corpia_globals import trace, converse_trace
from corpia_trace import corpia_trace

import csv

def call_llm (model, system_prompt, user_prompt):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("SECRET_KEY"))
    simulation = False

    if simulation is False:
        response = client.chat.completions.create(
            model = model,  # or another available model
            messages=[{
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": user_prompt
            }],
            temperature=0)
        return response.choices[0].message.content
    else:
        response = "This is the simulation response"
        return response


def call_llm_simple (model, system_prompt, user_prompt):
    load_dotenv()
    client = OpenAI(api_key=os.getenv("SECRET_KEY"))
    simulation = False

    if simulation is False:
        response = client.chat.completions.create(
            model=model,  # or another available model
            messages=[{
                "role": "system",
                "content": system_prompt
            }, {
                "role": "user",
                "content": user_prompt
            }],
            temperature=0)
        return response.choices[0].message.content
    else:
        response = "This is the simulation response"
        return response


import json
from datetime import datetime


schema_definition = """
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "processFlow": {
      "type": "array",
      "items": { "$ref": "#/definitions/activity" }
    }
  },
  "required": ["processFlow"],
  "additionalProperties": false,
  "definitions": {
    "activity": {
      "oneOf": [
        { "$ref": "#/definitions/invokeActivity" },
        { "$ref": "#/definitions/ifActivity" }
      ]
    },
    "invokeActivity": {
      "type": "object",
      "properties": {
        "invoke": {
          "type": "object",
          "properties": {
            "partnerLink": { "type": "string" },
            "operation": { "type": "string" },
            "currentDraft": { "type": "string" },
            "inputVariable": {
                        "type": "array",
                        "items": { "type": "string" }
                },
            "outputVariable": { "type": "string" },
            "description": { "type": "string" },
            "detailedDescription": { "type": "string" }
          },
          "required": [
            "partnerLink",
            "operation",
            "currentDraft",
            "inputVariable",
            "outputVariable"
          ],
          "additionalProperties": false
        }
      },
      "required": ["invoke"],
      "additionalProperties": false
    },
    "ifActivity": {
      "type": "object",
      "properties": {
        "if": {
          "type": "object",
          "properties": {
            "condition": { "type": "string" },
            "activities": {
              "type": "array",
              "items": { "$ref": "#/definitions/activity" }
            }
          },
          "required": ["condition", "activities"],
          "additionalProperties": false
        }
      },
      "required": ["if"],
      "additionalProperties": false
    }
  }
}

"""



def execute_process_flow(process_flow):
    # Simulated data store for variables
    variables = {}
    day_of_week = datetime.now().strftime('%A')

    for step in process_flow:
        if 'invoke' in step:
            invoke = step['invoke']
            partner_link = invoke.get('partnerLink')
            operation = invoke.get('operation')
            input_var = invoke.get('inputVariable')
            current_draft = invoke.get('currentDraft')
            description = invoke.get('description')
            detailed_description = invoke.get('detailedDescription')
            output_var = invoke.get('outputVariable')

            # Simulate the operation
            print(f"Invoking {operation} with {partner_link}")
            print(f"Input Variable: {input_var}")
            print(f"Output Variable: {output_var}")
            print(f"Current Draft: {current_draft}")
            print(f"Description: {description}")
            print(f"Details: {detailed_description}")

            input_string = ""
            if input_var == None:
                for input in input_var:
                    print(f"Input: {input}")
                    input_string = input_string + get_pairs_for_key(input)
                print(f"Input String: {input_string}")
            else:
                for input in input_var:
                    input_recall = get_pairs_for_key(input)
                    if input_recall is None:
                        input_string = "This is a Plug for Input"
                    else:
                        input_string = input_string + get_pairs_for_key(input)
                    print(f"Input String: {input_string}")

            # Simulate the operation
            print(f"Invoking {operation} with {partner_link}")
            print(f"Description: {description}")
            print(f"Details: {detailed_description}\n")

            if 'Review' in operation:
                prompt_string = ("The current version is: "
                                 + get_pairs_for_key(current_draft) +
                                 "The input is "
                                 + input_string +
                                 ", create an output based on this following request "
                                 + detailed_description)
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  prompt_string)
                add_pair(output_var, output)
                print(output)
            elif 'Feedback' in operation:
                prompt_string = ("The current version is: "
                                 + get_pairs_for_key(current_draft) +
                                 "The input is "
                                 + input_string +
                                 ", create an output based on this following request "
                                 + detailed_description)
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  prompt_string)
                add_pair(output_var, output)
                print(output)
            elif 'Update' in operation:
                prompt_string = ("The current version is: "
                                 + get_pairs_for_key(current_draft) +
                                 "The input is "
                                 + input_string +
                                 ", create an output based on this following request "
                                 + detailed_description)
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  prompt_string)
                add_pair(output_var, output)
                print(output)
            elif 'Create' in operation:
                prompt_string = ("The current version is: "
                                 + get_pairs_for_key(current_draft) +
                                 "The input is "
                                 + input_string +
                                 ", create an output based on this following request "
                                 + detailed_description)
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  prompt_string)
                add_pair(output_var, output)
                print(output)
            else:
                print(f"Unknown operation: {operation}")

            # Simulate input/output variables
#            variables[output_var] = f"{partner_link}_{operation}_Result"

        elif 'if' in step:
            condition = step['if'].get('condition')
            activities = step['if'].get('activities', [])

            # Evaluate the condition
            condition_result = evaluate_condition(condition, day_of_week)

            if condition_result:
                print(f"Condition '{condition}' is True. Executing activities inside 'if' block.\n")
                # Execute activities inside 'if'
                execute_process_flow(activities)
            else:
                print(f"Condition '{condition}' is False. Skipping 'if' block.\n")

        elif 'else' in step:
            # 'else' handling can be implemented if needed
            pass

def evaluate_condition(condition, current_day):
    # Simple condition evaluator for "Day == 'Sunday'"
    if condition.startswith("Day =="):
        day_to_compare = condition.split("==")[1].strip().strip("'\"")
        return current_day == day_to_compare
    return False

string_pairs = {}

# Function to add a pair of strings
def add_pair(s1, s2):
    if s1 in string_pairs:
        string_pairs[s1].add(s2)
    else:
        string_pairs[s1] = set([s2])
    print(f"Added pair: {{{s1}, {s2}}}")

# Function to remove a specific pair of strings
def remove_pair(s1, s2):
    if s1 in string_pairs and s2 in string_pairs[s1]:
        string_pairs[s1].remove(s2)
        if not string_pairs[s1]:  # If the set is empty, remove the key
            del string_pairs[s1]
        print(f"Removed pair: {{{s1}, {s2}}}")
    else:
        print(f"Pair {{{s1}, {s2}}} not found.")

# Function to check if a specific pair exists
def has_pair(s1, s2):
    return s1 in string_pairs and s2 in string_pairs[s1]

# Function to get all pairs for a given key
# def get_pairs_for_key(s1):
#    return_string_pairs = string_pairs.get(s1, set())
#    return return_string_pairs[0][1]

def get_pairs_for_key(s1):
    return_string_pairs = string_pairs.get(s1, set())
    # Convert the set to a list to enable indexing
    return_string_pairs = list(return_string_pairs)
    if return_string_pairs:
        return return_string_pairs[0]
    else:
        # Handle the case where the list is empty
        return None  # or any default value you prefer

# Function to print all pairs
def print_pairs():
    print("Current pairs:")
    for s1, s2_set in string_pairs.items():
        for s2 in s2_set:
            print(f"{{{s1}, {s2}}}")
    if not string_pairs:
        print("No pairs to display.")

def ppl_to_bpel (model, ppl_text):
    output_text = call_llm(model,
             "You are a translator from a Policy text to a BPEL implementation",
             ppl_text)
    return output_text


available_agents_prompt = """
The available agents are the CIO, the CEO, a McKinsey bank consultant, an internal bank strategy consultant, an economist, a lawyer and a communication specialist. Please use all of the roles in the process. 

"""

bpel_flow_prompt = """
For the task outlined below. Write the business process flow for this task. Write the flow in BPEL using the agents. Output only the JSON in this format and in one JSON block. Use this schema and follow the schema carefully to write the JSON process. Make sure the output string is JUST the JSON string.

The topmost element of the JSON is processFLow.

Ensure that outputs from one part of the process are the inputs to another part of the process.

Please return only JSON without any additional text or comments.

"""

language_prompt = """
The activity can be one of "invoke" and “if”.
One of the parameters for every Invoke activity must be "currentDraft"
The operation is one of Create, Review, Feedback or Update
- Create takes a set of inputVariables and creates an outputVariable based on the detailedDescription
- Review takes a set of inputVariables and creates an outputVariable which is a review of the inputVariable
- Feedback takes a set of inputVariable and creates an outputVariable which is a review of the inputVariable
- Update takes a set of inputVariable inputs to create an outputVariables

Have no spaces in the names of the inputVariable, outputVariable or currentDraft.
"""

task_prompt = """
Task:
Create a technology strategy for a large multinational bank:
Gather input on targets from the CEO
Gather input from the CIO in priorities
Gather input from the McKinsey bank consulant on industry trends
The internal strategy consultant will create the initial strategy version based on the inputs from the CEO, the CIO and the McKinsey bank consultant
5. Get feedback from the McKinsey consultant and the CIO
6. Create a version of the strategy with all the feedback
7. Final Legal review by the lawyer
8. Present to all employees

"""


def run_ppl(procedure_string):

    add_pair ("Targets", "Grow market share faster than competitors. Grow internationally.")
    add_pair ("Priorities", "Stay ahead of competitors technically. Maintain strong regulatory posture. Control costs")
    add_pair ("IndustryTrends", "Generative AI is growing. FinTechs are leading innovation ")
    add_pair ("InitialStrategyDraft", "")

    model = "gpt-4o-mini"
    bpel_string = call_llm_simple(model,
                                  "You are a system to generate simplified BPEL language in JSON",
                                  available_agents_prompt +
                    bpel_flow_prompt +
                    schema_definition +
                    language_prompt +
                    task_prompt)
    print ("BPEL string: " + bpel_string)

    data = json.loads(bpel_string)

    try:
        schema_json = json.loads(schema_definition)
        jsonschema.validate(data, schema_json)
        print("Data is valid")
    except jsonschema.exceptions.ValidationError as e:
        print("Data is invalid:", e.message)

    execute_process_flow(data['processFlow'])

    print_pairs()

if __name__ == '__main__':

    run_ppl("")

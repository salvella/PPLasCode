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

ppl_hr = """
The company always requires legal reviews at the end of the process.

The available agents are a Lawyer, Administrator, a First Line Manager, an HR Administrator and a Senior Manager.

For the task outlined below. Write the business process flow for this task. Write the flow in BPEL using the agents. Output only the JSON in this format and in one JSON block.

An example would be:

{
    "processFlow": [
        {
            "invoke": {
                "partnerLink": "FirstLineManager",
                "operation": "MonitorLeaveUsage",
                "inputVariable": "LeaveRecords",
                "outputVariable": "LeaveUsageReport",
                "description": "The First Line Manager monitors leave usage within their section, identifying patterns or significant absenteeism.",
                "detailedDescription": "The First Line Manager analyzes LeaveRecords to identify employees with significant absenteeism or unusual patterns of leave usage."
            }
        },
        {
            "invoke": {
                "partnerLink": "Administrator",
                "operation": "PerformLegalReview",
                "inputVariable": "ProcessDocumentation",
                "outputVariable": "LegalReviewComments",
                "description": "The Administrator performs a legal review of the absenteeism management process to ensure compliance.",
                "detailedDescription": "The Administrator reviews the entire process documentation to ensure it complies with legal and regulatory requirements, identifying any potential legal risks."
            }
        }
    ]
}
    
where the command can be one of "invoke", "review", "modify"

Task:
3.11 Absenteeism
(a) The management of innocent absenteeism is really a matter of
performance management. While the issues relating to
absenteeism are unique, the employer response in cases of
significant absenteeism is non-disciplinary and is provided in the
context of the desire for improved performance.
(b) As an element of performance, it is clearly appropriate to speak
with employees regarding their absenteeism in the context of
performance development.
(c) The absences requiring close monitoring include sick leave, injury
on duty leave, and special leave related to family illness. For cases
where the employee does not appear to have an on-going
disability, the employer should determine whether anything at work
is causing or contributing to the absences. The employee should
be asked about this and given an opportunity to indicate whether
anything at work or elsewhere in their life is causing them
difficulties. A sudden increase in sick and special leave usage may
be an indicator of the onset of a disability such as substance abuse
or of problems in the employee’s personal life.
(d) Employees are not obligated to divulge information relating to their
personal lives but they do have an obligation to actively deal with
any barriers to satisfactory work performance.
S If it appears appropriate, or you sense an underlying
problem that the employee will not speak with you about,
discuss E.A.P. with the employee. (See Section 8.06)
(e) General principles for Leave Management:
  monitor section, department and civil service leave usage;
  raise matter with employee as soon as issue appears;
  ensure clarity and verification of all leave requests and
supporting information;
  make periodic contact with employee during lengthy
absence; and
  E.A.P. referral where appropriate.
(f) To be successful at leave management, the employer must
approach the issue from the dual concerns of the employee’s wellbeing
and the work unit’s productivity and efficiency. While these
concerns may seem to be to some degree in conflict, the employer
needs to understand that neither of these is an absolute and that
the task is to strike an appropriate balance between the two.
(g) The most critical question in attempting to strike this balance is
whether the employee suffers from a disability which in turn gives
rise to the employer’s duty to accommodate.
"""

ppl_strategy = """
The company always requires legal reviews at the end of the process.

The available agents are the CIO, the CEO, a McKinsey bank consultant, an iternal bank strategy consultant, an economist, a lawyer and a communication specialist. Please use all of the roles in the process.

For the task outlined below. Write the business process flow for this task. Write the flow in BPEL using the agents. Output only the JSON in this format and in one JSON block.

An example would be:

{
    "processFlow": [
        {
            "invoke": {
                "partnerLink": "FirstLineManager",
                "operation": "MonitorLeaveUsage",
                "inputVariable": "LeaveRecords",
                "outputVariable": "LeaveUsageReport",
                "description": "The First Line Manager monitors leave usage within their section, identifying patterns or significant absenteeism.",
                "detailedDescription": "The First Line Manager analyzes LeaveRecords to identify employees with significant absenteeism or unusual patterns of leave usage."
            }
        },
        {
            "invoke": {
                "partnerLink": "Administrator",
                "operation": "PerformLegalReview",
                "inputVariable": "ProcessDocumentation",
                "outputVariable": "LegalReviewComments",
                "description": "The Administrator performs a legal review of the absenteeism management process to ensure compliance.",
                "detailedDescription": "The Administrator reviews the entire process documentation to ensure it complies with legal and regulatory requirements, identifying any potential legal risks."
            }
        }
    ]
}

where the command can be one of "invoke", "review", "modify"

Task:
Create a technology strategy for a large multinational bank:
(a) Gather feedback from all stakeholders
(b) Create a technology strategy
(c) Review the technology strategy with all stakeholders
(d) Modify the technology stratgey from the inputs
(e) Final legal review
(f) Create the communications to all employees
"""

ppl__hr_json = """
{
    "processFlow": [
        {
            "invoke": {
                "partnerLink": "FirstLineManager",
                "operation": "InitiateAbsenteeismManagement",
                "inputVariable": "AbsenteeismData",
                "outputVariable": "PerformanceImprovementPlan",
                "description": "The First Line Manager initiates management of absenteeism as part of performance management.",
                "detailedDescription": "The First Line Manager addresses absenteeism patterns and initiates discussion with employees on improving their performance by managing their absenteeism."
            }
        },
        {
            "invoke": {
                "partnerLink": "FirstLineManager",
                "operation": "ConductEmployeeInterview",
                "inputVariable": "EmployeeLeaveRecords",
                "outputVariable": "InterviewFeedback",
                "description": "The First Line Manager speaks with the employee regarding absenteeism in the context of performance development.",
                "detailedDescription": "The First Line Manager holds an interview with the employee to discuss ongoing absenteeism and explores potential work-related or personal factors affecting attendance."
            }
        },
        {
            "invoke": {
                "partnerLink": "HRAdministrator",
                "operation": "MonitorLeavePatterns",
                "inputVariable": "LeaveRecords",
                "outputVariable": "LeavePatternReport",
                "description": "The HR Administrator monitors leave patterns to identify trends related to sick leave and special leaves.",
                "detailedDescription": "HR Administrator reviews LeaveRecords to monitor patterns of sick leave, injury on duty leave, and special leave related to family illness, reporting findings to management."
            }
        },
        {
            "invoke": {
                "partnerLink": "Administrator",
                "operation": "VerifyLeaveRequests",
                "inputVariable": "LeaveRequests",
                "outputVariable": "VerifiedLeaveRequests",
                "description": "The Administrator ensures clarity and verification of all leave requests.",
                "detailedDescription": "The Administrator carefully verifies the authenticity and completeness of all LeaveRequests and ensures supporting information is accurate."
            }
        },
        {
            "invoke": {
                "partnerLink": "FirstLineManager",
                "operation": "EngageEAP",
                "inputVariable": "EmployeeConcerns",
                "outputVariable": "EAPReferral",
                "description": "Discuss Employee Assistance Program (EAP) with employee if underlying problems are sensed.",
                "detailedDescription": "The First Line Manager engages with the EAP to assist the employee in discussing personal issues potentially impacting their work performance."
            }
        },
        {
            "invoke": {
                "partnerLink": "SeniorManager",
                "operation": "BalanceWorkAndWellbeing",
                "inputVariable": "OutcomeReports",
                "outputVariable": "BalancedStrategy",
                "description": "The Senior Manager develops a strategy to balance employee well-being with productivity and efficiency.",
                "detailedDescription": "The Senior Manager assesses the collaborative reports to ensure a balance between employee well-being and the work unit’s productivity and efficiency."
            }
        },
        {
            "review": {
                "partnerLink": "Lawyer",
                "operation": "LegalComplianceCheck",
                "inputVariable": "ProcessDocumentation",
                "outputVariable": "LegalReviewOutcome",
                "description": "The Lawyer performs a legal review to ensure compliance with employment laws related to absenteeism management.",
                "detailedDescription": "The Lawyer reviews the absenteeism management process documentation to ensure compliance with all relevant legal and regulatory frameworks, highlighting any potential legal issues."
            }
        }
    ]
}
"""

ppl_strategy_json = """
{
    "processFlow": [
        {
            "invoke": {
                "partnerLink": "CIO",
                "operation": "GatherStakeholderFeedback",
                "inputVariable": "StakeholdersFeedbackForm",
                "outputVariable": "StakeholderFeedback",
                "description": "The CIO gathers feedback from all stakeholders regarding the current technology practices and expectations.",
                "detailedDescription": "The CIO collects input from various stakeholders using surveys and feedback forms to understand their needs and expectations on technology."
            }
        },
        {
            "invoke": {
                "partnerLink": "CEO",
                "operation": "CreateTechnologyStrategy",
                "inputVariable": "StakeholderFeedback",
                "outputVariable": "DraftTechnologyStrategy",
                "description": "The CEO develops an initial technology strategy based on the gathered stakeholder feedback.",
                "detailedDescription": "The CEO combines insights from stakeholder feedback to draft a comprehensive technology strategy for the bank."
            }
        },
        {
            "review": {
                "partnerLink": "McKinseyBankConsultant",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "DraftTechnologyStrategy",
                "outputVariable": "ConsultantFeedback",
                "description": "The McKinsey Bank Consultant reviews the technology strategy and provides expert insights.",
                "detailedDescription": "The McKinsey Bank Consultant examines the draft strategy to ensure its alignment with industry best practices and offers recommendations for improvement."
            }
        },
        {
            "review": {
                "partnerLink": "InternalBankStrategyConsultant",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "DraftTechnologyStrategy",
                "outputVariable": "InternalFeedback",
                "description": "The Internal Bank Strategy Consultant reviews the technology strategy to ensure alignment with internal business goals.",
                "detailedDescription": "The Internal Strategy Consultant evaluates the strategy for compatibility with the bank's internal objectives and suggests any adjustments needed."
            }
        },
        {
            "review": {
                "partnerLink": "Economist",
                "operation": "EvaluateEconomicImplications",
                "inputVariable": "DraftTechnologyStrategy",
                "outputVariable": "EconomicFeedback",
                "description": "The Economist assesses the economic impact and feasibility of the proposed technology strategy.",
                "detailedDescription": "The Economist analyzes the strategy to predict its economic outcome and advises on sustainable implementation methods."
            }
        },
        {
            "modify": {
                "partnerLink": "CIO",
                "operation": "IncorporateFeedback",
                "inputVariable": "ConsultantFeedback, InternalFeedback, EconomicFeedback",
                "outputVariable": "RevisedTechnologyStrategy",
                "description": "The CIO modifies the technology strategy based on the collected feedback from various experts and stakeholders.",
                "detailedDescription": "The CIO adjusts the technology plan, incorporating feedback from both external and internal consultations to refine and enhance the strategy."
            }
        },
        {
            "review": {
                "partnerLink": "Lawyer",
                "operation": "PerformLegalReview",
                "inputVariable": "RevisedTechnologyStrategy",
                "outputVariable": "LegalReviewComments",
                "description": "The Lawyer performs a final legal review on the revised technology strategy.",
                "detailedDescription": "The Lawyer ensures that the strategy adheres to all relevant laws and regulatory requirements, identifying any legal considerations."
            }
        },
        {
            "invoke": {
                "partnerLink": "CommunicationSpecialist",
                "operation": "CreateEmployeeCommunication",
                "inputVariable": "RevisedTechnologyStrategy",
                "outputVariable": "EmployeeCommunication",
                "description": "The Communication Specialist creates the communication materials to be shared with all employees about the new technology strategy.",
                "detailedDescription": "The Communication Specialist drafts and prepares materials explaining the new technology strategy to all employees, ensuring clarity and engagement."
            }
        }
    ]
}
"""

import json
from datetime import datetime

# The JSON process flow provided
process_flow_json = '''
{
    "processFlow": [
        {
            "invoke": {
                "partnerLink": "CIO",
                "operation": "ProvideFeedback",
                "inputVariable": "FeedbackRequest",
                "outputVariable": "CIOFeedback",
                "description": "Gather feedback from the CIO on technology strategy.",
                "detailedDescription": "Request the CIO to provide their insights and feedback on the upcoming technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "CEO",
                "operation": "ProvideFeedback",
                "inputVariable": "FeedbackRequest",
                "outputVariable": "CEOFeedback",
                "description": "Gather feedback from the CEO on technology strategy.",
                "detailedDescription": "Request the CEO to provide their strategic vision and feedback on the technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "McKinseyConsultant",
                "operation": "ProvideFeedback",
                "inputVariable": "FeedbackRequest",
                "outputVariable": "McKinseyFeedback",
                "description": "Gather feedback from the McKinsey bank consultant on technology strategy.",
                "detailedDescription": "Request the external McKinsey bank consultant to provide their expert feedback on the technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "InternalStrategyConsultant",
                "operation": "ProvideFeedback",
                "inputVariable": "FeedbackRequest",
                "outputVariable": "InternalConsultantFeedback",
                "description": "Gather feedback from the internal bank strategy consultant on technology strategy.",
                "detailedDescription": "Request the internal bank strategy consultant to provide their insights and feedback on the technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "Economist",
                "operation": "ProvideFeedback",
                "inputVariable": "FeedbackRequest",
                "outputVariable": "EconomistFeedback",
                "description": "Gather feedback from the economist on technology strategy.",
                "detailedDescription": "Request the economist to provide economic analysis and feedback on the technology strategy."
            }
        },
        {
            "if": {
                "condition": "Day == 'Sunday'",
                "activities": [
                    {
                        "invoke": {
                            "partnerLink": "Pope",
                            "operation": "ProvideFeedback",
                            "inputVariable": "FeedbackRequest",
                            "outputVariable": "PopeFeedback",
                            "description": "Ask the Pope for feedback on the technology strategy if it's Sunday.",
                            "detailedDescription": "If today is Sunday, request the Pope to provide his insights and blessings on the technology strategy."
                        }
                    }
                ]
            }
        },
        {
            "invoke": {
                "partnerLink": "CIO",
                "operation": "CreateTechnologyStrategy",
                "inputVariable": "StakeholderFeedback",
                "outputVariable": "TechnologyStrategyDraft",
                "description": "CIO creates the initial draft of the technology strategy.",
                "detailedDescription": "Using the feedback collected from stakeholders, the CIO develops the initial draft of the technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "CEO",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "TechnologyStrategyDraft",
                "outputVariable": "CEOReviewComments",
                "description": "CEO reviews the technology strategy.",
                "detailedDescription": "The CEO reviews the drafted technology strategy and provides comments."
            }
        },
        {
            "invoke": {
                "partnerLink": "McKinseyConsultant",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "TechnologyStrategyDraft",
                "outputVariable": "McKinseyReviewComments",
                "description": "McKinsey consultant reviews the technology strategy.",
                "detailedDescription": "The McKinsey bank consultant reviews the drafted technology strategy and provides expert comments."
            }
        },
        {
            "invoke": {
                "partnerLink": "InternalStrategyConsultant",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "TechnologyStrategyDraft",
                "outputVariable": "InternalConsultantReviewComments",
                "description": "Internal strategy consultant reviews the technology strategy.",
                "detailedDescription": "The internal bank strategy consultant reviews the drafted technology strategy and provides comments."
            }
        },
        {
            "invoke": {
                "partnerLink": "Economist",
                "operation": "ReviewTechnologyStrategy",
                "inputVariable": "TechnologyStrategyDraft",
                "outputVariable": "EconomistReviewComments",
                "description": "Economist reviews the technology strategy.",
                "detailedDescription": "The economist reviews the drafted technology strategy and provides comments on economic implications."
            }
        },
        {
            "modify": {
                "partnerLink": "CIO",
                "operation": "UpdateTechnologyStrategy",
                "inputVariable": "AllReviewComments",
                "outputVariable": "TechnologyStrategyFinal",
                "description": "CIO modifies the technology strategy based on stakeholder inputs.",
                "detailedDescription": "The CIO incorporates feedback from all stakeholders to update and finalize the technology strategy."
            }
        },
        {
            "invoke": {
                "partnerLink": "Lawyer",
                "operation": "PerformLegalReview",
                "inputVariable": "TechnologyStrategyFinal",
                "outputVariable": "LegalApproval",
                "description": "Lawyer performs a final legal review of the technology strategy.",
                "detailedDescription": "The lawyer reviews the finalized technology strategy to ensure compliance with legal and regulatory requirements."
            }
        },
        {
            "invoke": {
                "partnerLink": "CommunicationSpecialist",
                "operation": "CreateEmployeeCommunication",
                "inputVariable": "TechnologyStrategyFinal",
                "outputVariable": "EmployeeCommunication",
                "description": "Communication specialist prepares communications to all employees.",
                "detailedDescription": "Using the finalized technology strategy, the communication specialist drafts messages to inform all employees about the new strategy."
            }
        }
    ]
}
'''

new_process_flow2 = """
{
  "processFlow": [
    {
      "invoke": {
        "partnerLink": "CIO",
        "operation": "CreateDraftStrategy",
        "inputVariable": "BusinessObjectives",
        "outputVariable": "DraftStrategy",
        "description": "The CIO creates a draft of the technology strategy for the bank.",
        "detailedDescription": "The CIO develops an initial draft of the technology strategy based on the bank's business objectives and technological needs."
      }
    },
    {
      "invoke": {
        "partnerLink": "CEO",
        "operation": "ReviewStrategy",
        "inputVariable": "DraftStrategy",
        "outputVariable": "CEOReviewComments",
        "description": "The CEO reviews the draft strategy and provides comments.",
        "detailedDescription": "The CEO assesses the draft strategy in terms of alignment with the overall business vision and goals."
      }
    },
    {
      "invoke": {
        "partnerLink": "McKinseyConsultant",
        "operation": "ReviewStrategy",
        "inputVariable": "DraftStrategy",
        "outputVariable": "McKinseyConsultantReviewComments",
        "description": "The McKinsey bank consultant reviews the draft strategy and provides comments.",
        "detailedDescription": "The McKinsey consultant offers expert insights and industry best practices to enhance the strategy."
      }
    },
    {
      "invoke": {
        "partnerLink": "InternalStrategyConsultant",
        "operation": "ReviewStrategy",
        "inputVariable": "DraftStrategy",
        "outputVariable": "InternalConsultantReviewComments",
        "description": "The internal bank strategy consultant reviews the draft strategy and provides comments.",
        "detailedDescription": "The internal consultant ensures the strategy aligns with internal policies and strategic directions."
      }
    },
    {
      "invoke": {
        "partnerLink": "Economist",
        "operation": "ReviewStrategy",
        "inputVariable": "DraftStrategy",
        "outputVariable": "EconomistReviewComments",
        "description": "The Economist reviews the draft strategy and provides comments.",
        "detailedDescription": "The Economist analyzes the strategy's economic implications and forecasts."
      }
    },
    {
      "invoke": {
        "partnerLink": "CommunicationSpecialist",
        "operation": "ReviewStrategy",
        "inputVariable": "DraftStrategy",
        "outputVariable": "CommunicationSpecialistReviewComments",
        "description": "The Communication Specialist reviews the draft strategy and provides comments.",
        "detailedDescription": "The Communication Specialist ensures the strategy is clearly articulated and communication-ready."
      }
    },
    {
      "if": {
        "condition": "Day is Sunday",
        "activities": [
          {
            "invoke": {
              "partnerLink": "Pope",
              "operation": "ReviewStrategy",
              "inputVariable": "DraftStrategy",
              "outputVariable": "PopeReviewComments",
              "description": "The Pope reviews the draft strategy and provides comments.",
              "detailedDescription": "On Sundays, the Pope offers spiritual and ethical guidance on the technology strategy."
            }
          }
        ]
      }
    },
    {
      "modify": {
        "targetVariable": "DraftStrategy",
        "operation": "UpdateWithComments",
        "inputVariables": [
          "CEOReviewComments",
          "McKinseyConsultantReviewComments",
          "InternalConsultantReviewComments",
          "EconomistReviewComments",
          "CommunicationSpecialistReviewComments",
          "PopeReviewComments"
        ],
        "outputVariable": "UpdatedStrategy",
        "description": "The CIO updates the strategy with all review comments.",
        "detailedDescription": "The CIO consolidates feedback from all stakeholders and revises the strategy accordingly."
      }
    },
    {
      "invoke": {
        "partnerLink": "Lawyer",
        "operation": "PerformLegalReview",
        "inputVariable": "UpdatedStrategy",
        "outputVariable": "LegalReviewComments",
        "description": "The Lawyer performs a legal review of the updated strategy.",
        "detailedDescription": "The Lawyer ensures that the strategy complies with all legal and regulatory requirements."
      }
    }
  ]
}
"""

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
        { "$ref": "#/definitions/ifActivity" },
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
            "inputVariable": { "type": "string" },
            "outputVariable": { "type": "string" },
            "description": { "type": "string" },
            "detailedDescription": { "type": "string" }
          },
          "required": [
            "partnerLink",
            "operation",
            "inputVariable",
            "outputVariable",
            "description",
            "detailedDescription"
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
    },
  },
}
"""

prompt_bpel_preable = """
For the task outlined below write the business process flow for this task. Write the flow in BPEL using the agents. Output only the JSON in this format and in one JSON block.
Use this schema as output for the BPEL process flow. 

"""

prompt_bpel_question = """

where the command can be one of “invoke" or “if”

Review each step and make sure it is clear what the inputs required are and what are the actions required and what are the outputs.

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
            input_vars = invoke.get('inputVariables')
            description = invoke.get('description')
            detailed_description = invoke.get('detailedDescription')
            output_var = invoke.get('outputVariable')

            # Simulate the operation
            print(f"Invoking {operation} with {partner_link}")
            print(f"Input Variable: {input_var}")
            print(f"Description: {description}")
            print(f"Details: {detailed_description}\n")

            input_string = ""
            if input_var == None:
                for input in input_vars:
                    print(f"Input: {input}")
                    input_string = input_string + get_pairs_for_key(input)
                print(f"Input String: {input_string}")
            else:
                input_string = input_string + get_pairs_for_key(input_var)
                print(f"Input String: {input_string}")

            # Simulate the operation
            print(f"Invoking {operation} with {partner_link}")
            print(f"Description: {description}")
            print(f"Details: {detailed_description}\n")

            if 'Review' in operation:
                output = call_llm("gpt-4o-mini",
                         f"You are a {partner_link} agent",
                         f"Provide feedback: {detailed_description} on {input_string}")
                add_pair(output_var, output)
                print (output)
            elif 'Feedback' in operation:
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  f"Provide feedback on: {detailed_description} on {input_string}")
                add_pair(output_var, output)
                print(output)
            elif 'Create' in operation:
                output = call_llm("gpt-4o-mini",
                                  f"You are a {partner_link} agent",
                                  f"Create a: {detailed_description})")
                add_pair(output_var, output)
                print(output)
            else:
                print(f"Unknown operation: {operation}")

            # Simulate input/output variables
#            variables[output_var] = f"{partner_link}_{operation}_Result"

        elif 'modify' in step:
            modify = step['modify']
            partner_link = modify.get('partnerLink')
            operation = modify.get('operation')
            input_var = modify.get('inputVariable')
            input_vars = modify.get('inputVariables')
            input_string = ""
            if input_var == None:
                for input in input_vars:
                    print(f"Input: {input}")
                    input_string = input_string + get_pairs_for_key(s1)
                print(f"Input String: {input_string}")
            else:
                input_string = input_string + get_pairs_for_key(s1)
                print(f"Input String: {input_string}")
            output_var = modify.get('outputVariable')
            description = modify.get('description')
            detailed_description = modify.get('detailedDescription')

            # Simulate the modification
            print(f"Modifying with {operation} by {partner_link}")
            print(f"Description: {description}")
            print(f"Details: {detailed_description}\n")
            print(f"InputVariable: {input_var}")
            if input_var == None:
                for input in input_vars:
                    print(f"Input: {input}")

            # Simulate input/output variables
            variables[output_var] = f"{partner_link}_{operation}_Result"

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

prompt_checker = """
You are a checker of policy and procedures. You look for errors and omissions. 

Here are some of the details you should include in a conflict of interest policy:
	A statement about an individual’s duty to disclose any conflicts of interest
	The process for reviewing potential conflicts of interest
	Details about disciplinary actions for violating the policy
	A disclosure statement that’s signed by all board members, staff members, and other key personnel each year
The policy should also should include the following details:
	A definition of what constitutes a conflict of interest
	Procedures for disclosing a conflict of interest to the appropriate leaders
	A requirement that the person with the conflict should not be present at or participate in deliberation or vote on the matter
	A prohibition against any attempt by the person to improperly influence the deliberation or voting on the matter related to the conflict
	A requirement that the existence and resolution of the conflict of interest be documented in the corporation’s records
	Procedures for disclosing, addressing, and documenting related transactions


Major errors are omissions which may be missing a step or phrases that are ambiguous or confusing. Minor errors are suggestions to improve the text. Review the following text and list the major and minor errors. 
"""

prompt_fixer = """
Correct the Policy and re-write the policy fixing each of the problems
"""



def run_ppl(name):

    model = "gpt-4o"

    output_trace = corpia_trace(name)

    output_trace.corpia_trace(name, 1, 1, "")

    output_trace.corpia_trace(name, 3, 1, "Execute Batch File")
    output_trace.corpia_trace(name, 3, 1, "Model: \n" + model)

    filename = "./batch/" + name + ".csv"
    csv_file = open(filename, 'r')
    reader = csv.reader(csv_file)

    for row in reader:
        print ("Organization: \n" + row[0])
#       print ("Name: \n" + row[1])
        output_trace.corpia_trace(row[0], 3, 1,"Organization: \n" + row[0])
        output_trace.corpia_trace(row[0], 3, 1,"Policy: \n" + row[1])

        history = ""
        output = ""

# Step 1: Check the Policy for Errors

        prompt = prompt_checker + row[1]
        history = prompt + output
        output_trace.corpia_trace(row[0], 3, 1, "Checker Prompt: \n" + prompt)
        output = call_llm (model, "You are a helpful agent" + history, prompt)
        output_trace.corpia_trace(row[0], 3, 1, "Checker: \n" + output)

# Step 2: Fix the Policy based on the errors

        history = history + prompt + output
        prompt = prompt_fixer + output
        output_trace.corpia_trace(row[0], 3, 1, "Fixer Prompt: \n" + prompt)
        output = call_llm (model, history, prompt)
        output_trace.corpia_trace(row[0], 3, 1, "Fixed: \n" + output)

# Step 3: Create the BPEL


        history = history + prompt + output
        prompt = prompt_bpel_preable + schema_definition + prompt_bpel_question + output
        output_trace.corpia_trace(row[0], 3, 1, "BPEL Creator: \n" + prompt)
        output = call_llm (model, history, prompt)
        output_trace.corpia_trace(row[0], 3, 1, "BPEL: \n" + output)

# Step 4: Roundtrip back to Natural Language

        prompt_create_policy = "Using the BPEL provided, create the procedure in English for this policy. Think step by step: "

        history = history + prompt + output
        prompt = prompt_create_policy + output
        output_trace.corpia_trace(row[0], 3, 1, "Policy Creator: \n" + prompt)
        output = call_llm(model, history, prompt)
        output_trace.corpia_trace(row[0], 3, 1, "Policy: \n" + output)

    output_trace.corpia_trace(name, 2, 1, "")

if __name__ == '__main__':

#   print(ppl_to_bpel ("gpt-4o-2024-08-06", ppl_strategy))

    # add_pair("BusinessObjectives", "Be the technology company with a bank logo")
    # Load the JSON data

    run_ppl("COIPolicy")

#    data = json.loads(new_process_flow2)
#    print (jsonschema.validate(data, json.loads(schema_definition)))


    # Execute the process flow
    # execute_process_flow(data['processFlow'])

    #add_pair("A", "Apple")
    #add_pair("B", "Bean")
    #print_pairs()
    #print(get_pairs_for_key("A"))
    #print(get_pairs_for_key("B"))

    #print("OUTPUTS:")
    #print_pairs()


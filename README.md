# PPLasCode
 **Policy and Procedure Library as Code**

This is a repository of materials associated with the paper "Policy and Procedure as Code".

The following files are here:

**COIPolicy.csv**

This is the set of Conflict of Interest policies that will be processed. This is presented as an .CSV file and is used by the Python program as an input.

Follow on work will focus on:

* Additional policies other than Conflict of Interest
* More complex policies and interdependent policies

**COIPolicy-Processed.csv**

This is the output, in .CSV format of processing of the Conflict of Interest policies in the COIPolicy.csv files.

This file was processed using gpt-4o.

Follow on work will include:

* Work with additional AI models to compare results
* Creation of a benchmark on reasoning through policy and procedure

**PPLPaper.py**

Python code to execute the policy checking, conversion to BPEL and convert the BPEL to the policy.

Key assets in the code:

* LLM parameters - Temperature=0
* Model used is gpt-4o but is an easy to change parameter
* Prompts used
* Simplified BPEL schema definition
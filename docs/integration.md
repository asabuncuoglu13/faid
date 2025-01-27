# Integrate FAID into your codebase

We created the FAID repository to support developers quickly integrate metadata management into their codebase. You can keep using your current experiment tracking tools (e.g. [wandb](https://wandb.ai/site), [Neptune](https://neptune.ai/), [mlflow](https://mlflow.org/)), and record fairness-related data in a standardised and interoperable way. 

FAID is not a Python library. We don't want to abstract away the FAID features. Throughout the development process, developers should take some time and think about their model safety and how to monitor them. Then, they can directly include FAID source code to their codebases to customise FAID's functionality based on their needs. In this document, we shared the potential integration approaches:

## Logging

`📂 faid/logging` includes `📂 templates` and `📂 schema` for metadata storage, as well as utility files for initiating, populating and syncing metadata.

**Logging** is the core of FAID repository. It works on its own, and other functionalities depends on logging functions. S


## Reports

`📂 faid/report` includes `📂 templates` and utility files for generating reports using the metadata information. 


## Evaluation and Mitigation



## Complete FAID Integration



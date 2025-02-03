# FAID: Fair AI Development

> **Research Preview Disclaimer:** This repository contains code, data, and materials that are part of an ongoing research project. Please note that the work is in a **research preview** stage and may produce incomplete or inconsistent results. Use at your own discretion, and feel free to contribute or report any issues.

> See all demos: 

Achieving fairness in product development is a shared responsibility among all stakeholders, including developers, business analysts, product owners, designers, and user researchers. FAID aims to help development teams to share fairness and safety related metadata, risks, and transparency reports easily and quickly. FAID also includes some helper functions to integrate common fairness libraries and frameworks such as fairlearn, AISI's inspect_ai, WEFE (word embedding fairness), etc.

The main idea of FAID is illustrated in below diagram:

![](./docs/media/metadata.png)

Throughout the development lifecycle, a fairness log is recorded for very experiment, and it informs the model, data, risk and transparency logs in system level.

## Integrate FAID into your codebase

We created the FAID repository to support developers quickly integrate metadata management into their codebase. You can keep using your current experiment tracking tools (e.g. [wandb](https://wandb.ai/site), [Neptune](https://neptune.ai/), [mlflow](https://mlflow.org/)), and record fairness-related data in a standardised and interoperable way. 

FAID is not a Python library. We don't want to abstract away the FAID features. Throughout the development process, developers should take some time and think about their model safety and how to monitor them. Then, they can directly include FAID source code to their codebases to customise FAID's functionality based on their needs. In this document, we shared the potential integration approaches:

### Logging

`📂 faid/logging` includes `📂 templates` and `📂 schema` for metadata storage, as well as utility files for initiating, populating and syncing metadata.

**Logging** is the core of FAID repository. It works on its own, and other functionalities depends on logging functions. So, you should start with integrating it and understanding its capabilities.


### Reports

`📂 faid/report` includes `📂 templates` and utility files for generating reports using the metadata information. The reports visualise the metadata in a friendly graphical format. Think about customising these templates to increase the visibility of "safety considerations."


### Evaluation and Mitigation

`📂 faid/metrics` includes some commonly used evaluation metrics and a fairness-oriented sub-group discovery technique. You can use alternative metrics libraries (e.g. fairlearn, IBM Fair 360), and sub-group selection techniques.

`📂 faid/ner` provides named entity recognition (NER) functionality to train a custom NER model (using spacy), and use it for identifying entities of interest. You can use this method to understand potential unbalanced representations in a dataset.

`📂 faid/mitigation` includes a custom counterfactual sample generator method to kickstart your mitigation experiments. You can use it for assessing the model capabilities, and generate more balanced datasets for mitigating bias.


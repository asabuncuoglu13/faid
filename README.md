# Fair AI Development

> **Research Preview Disclaimer:** This repository contains code, data, and materials that are part of an ongoing research project. Please note that the work is in a **research preview** stage and may produce incomplete or inconsistent results. Use at your own discretion, and feel free to contribute or report any issues.

This repository showcases leveraging the use of metadata in fairness monitoring. 

> See all demos: [Demo List](./demos/README.md)

Achieving fairness in product development is a shared responsibility among all stakeholders, including developers, business analysts, product owners, designers, and user researchers. So, all parties need to actively feel the responsibility to share the design decisions with each other. This repository presents a set of useful functions and templates to support development teams to share fairness and safety related metadata, risks, and transparency reports. The demo tutorials showcases the use of common fairness libraries and frameworks such as fairlearn, AISI's inspect_ai, WEFE (word embedding fairness), etc.

![](./docs/media/metadata.png)

Throughout the development lifecycle, a fairness log is recorded for very experiment, and it informs the model, data, risk and transparency logs in system level.

## Logging fairness related metadata

- `📂 faid/logging` includes all logging-related functionalities such as initiating the metadata files, populating and syncing them. 
- `📂 faid/logging/templates` are empty YML files with the core metadata formats: Data, model, fairness, risks, and transparency.

> The metadata templates are available with descriptions. See [templates with example descriptions](./faid/logging/template_example_descriptions/).

![](./docs/media/metadataflow.png)

**Logging** is the core of this repository. All other functionalities (report and scan) depends on logging utilities. So, you should start with integrating it.

### Reporting

- `📂 faid/report` includes utility functions for generating reports. The reports visualise the metadata in a friendly graphical format.
- `📂 faid/report/schema` contains the ontology of fairness notions and metrics to create standardised visualisations.
- `📂 faid/report/templates` includes [Jinja](https://jinja.palletsprojects.com/en/stable/) templates for generating HTML templates for automatically translating the existing metadata to reports.

### Scanning

- `📂 faid/scan` includes utility functions that scan the popular safety benchmarks to find existing fairness scores of the pre-trained models (only LLMs).
- `📂 faid/scan/unit_tests` includes example data unit tests that you can use throughout the development process.

> See the [Docs](./docs/) for more details.

## Towards AI-enabled documentation

Keeping a record of data and model (e.g. collection practices, development details, transformation throughout the process) is essential to achieve a transparent governance. The rise of AI-enabled coding practices (e.g. Github Copilot, Cursor) can actually finally help us to achieve a step-by-step documentation. We are all aware that maintaining a good documentation and public artefacts such as model cards and datasheets depends on the development team's skillset and willingness. However, we've actually seen an increase in the good documentation practices, as AI-enabled helper tools in the process can automatically generate these docs. Then, we can update them quickly. 

However, a generic and non-standard documentation generated automatically by these tools would just be an illusion of transparency. A documentation standard that is structured based on safety and robustness characteristics defined by commonly used standards can support development and risk management teams in compliance process.

1. A set of standardised metadata formats are available in this repository;
2. AI-enabled copilot creates the first draft of the documentation using a project-level access;
3. The development team reviews the draft;
   a. Approved: The documentation is properly versioned and released,
   b. Revision required: Step by step, for each entity, analysis of the code and data to fill the required entities
4. When the first version is ready, entities can be updated after each merge is accepted.


## This repository is not...

- This repository is not a replacement of an existing experiment tracking library. Keep using your favourite experiment tracking tool (e.g. [wandb](https://wandb.ai/site), [Neptune](https://neptune.ai/), [mlflow](https://mlflow.org/)).  record fairness-related data in a standardised and interoperable way. These libraries allow you to record all the hyper-parameters and replicate the experiments. Here, in this research repository, our aim is to discover the **the right level of abstraction** to record model safety related information and share it with diverse stakeholders.
- This repository is not a Python library. We don't want to hide away the internal functions and metadata details. In contrary, we want to expose them and make them visible so that developers spend some time and think about their model safety and ways to monitor it. Then, they can directly include logging, reporting or scanning source code to their codebases to customise the functionality.


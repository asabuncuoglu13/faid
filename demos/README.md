# Keeping a Fairness Log in Different Settings

A fairness log does not only bound to bias evaluation and mitigation experiments. From dataset collection to model deployment, model and data related changes can be an interest of fairness metadata logging. 

Although the logging format and process is standardised for any ML development, the type and modality of data and model can require some tweaks in the recording procedure. Our demo notebooks aim to demonstrate the capabilities of FAID toolkit, and showcase how developers integrate it into their unique codebases.

## List of Tutorials

**Tabular Model - Evaluation:**
- [credit-scoring-fairlearn/demo_credit_loan_decisions.ipynb](demos/credit-scoring-fairlearn/demo_credit_loan_decisions.ipynb): Demonstrates fairness evaluation in credit loan decision models using the fairlearn library.
- [adult-subgroupdiscovery/fairsd_usage.ipynb](demos/adult-subgroupdiscovery/fairsd_usage.ipynb): Shows the usage of fairness-aware subgroup discovery in practice.

**Text Model - Evaluation:**
- [sentiment-analysis/demo-finbert.ipynb](demos/sentiment-analysis/demo-finbert.ipynb): Shows how to perform fairness evaluation of FinBERT sentiment analysis model.
- [embeddings-eval/WEAT.ipynb](demos/embeddings-eval/WEAT.ipynb): Evaluates word embeddings using the Word Embedding Association Test (WEAT).

**Text Model - Mitigation: (All work-in-progress)**
- [architecture-modification/adapter_tuning_FinSent.ipynb](demos/architecture-modification/adapter_tuning_FinSent.ipynb): Explains how to tune adapters for fair financial sentiment analysis.
- [embeddings-mitigate/BABE_debiasing_nullspace.ipynb](demos/embeddings-mitigate/BABE_debiasing_nullspace.ipynb): Demonstrates debiasing word embeddings of a media dataset.
- [embeddings-mitigate/use_debiasing.ipynb](demos/embeddings-mitigate/use_debiasing.ipynb): Shows how to use debiasing techniques on word embeddings.
- 
**Explainability and External Library Integration:**
- [captum-gradients/captum-integrated-gradients.ipynb](demos/captum-gradients/captum-integrated-gradients.ipynb): Illustrates the use of Captum's integrated gradients for model interpretability.
- [external-tools/demo-external-tools.ipynb](demos/external-tools/demo-external-tools.ipynb): Integrates external tools for fairness evaluation.
- [rag-giskard/RAGET_Banking_Supervision.ipynb](demos/rag-giskard/RAGET_Banking_Supervision.ipynb): Explores the use of Giskard and its integration with FAID in an illustrative RAG application for banking supervision.

**Data Unit Tests and RAI Fields:**
- [data-unit-tests/demo-data-unit-tests.ipynb](demos/data-unit-tests/demo-data-unit-tests.ipynb): Shows how to implement data unit tests for fairness.
- [rai-fields/demo-rai-logging.ipynb](demos/rai-fields/demo-rai-logging.ipynb): Demonstrates using the RAI fields of other metadata formats.
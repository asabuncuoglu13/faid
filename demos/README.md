# Keeping a Fairness Log in Different Settings

In this repository, we present a limited set of entities, that can accept information in multiple formats. Hence, we presented a set of tutorials to showcase recording fairness-oriented metadata for different model types, data modalities, and experiment tasks.

## Fairness Evaluation - Different Modalities

- **Tabular Model - Evaluation:** [credit-scoring-fairlearn/demo_credit_loan_decisions.ipynb](credit-scoring-fairlearn/demo_credit_loan_decisions.ipynb): Demonstrates fairness evaluation in credit loan decision models using the fairlearn library.
- **Text Model - Evaluation:** [sentiment-analysis/demo-finbert.ipynb](sentiment-analysis/demo-finbert.ipynb): Shows how to perform fairness evaluation of FinBERT sentiment analysis model.
- **Text Model - Embeddings:** [embeddings-eval/WEAT.ipynb](embeddings-eval/WEAT.ipynb): Evaluates word embeddings using the Word Embedding Association Test (WEAT).

- **Recording subgroups in the evaluation:** - [adult-subgroupdiscovery/fairsd_usage.ipynb](adult-subgroupdiscovery/fairsd_usage.ipynb): Shows the usage of fairness-aware subgroup discovery in practice.

## Fairness Mitigation

**Text Model - Mitigation: (All work-in-progress):**
- [architecture-modification/adapter_tuning_FinSent.ipynb](architecture-modification/adapter_tuning_FinSent.ipynb): Explains how to tune adapters for fair financial sentiment analysis.
- [embeddings-mitigate/BABE_debiasing_nullspace.ipynb](embeddings-mitigate/BABE_debiasing_nullspace.ipynb): Demonstrates debiasing word embeddings of a media dataset.
- [embeddings-mitigate/use_debiasing.ipynb](embeddings-mitigate/use_debiasing.ipynb): Shows how to use debiasing techniques on word embeddings.

## Explainability and Using External Libraries

- [captum-gradients/captum-integrated-gradients.ipynb](captum-gradients/captum-integrated-gradients.ipynb): Illustrates the use of Captum's integrated gradients for model interpretability.
- [external-tools/demo-external-tools.ipynb](external-tools/demo-external-tools.ipynb): Integrates external tools for fairness evaluation.
- [rag-giskard/RAGET_Banking_Supervision.ipynb](rag-giskard/RAGET_Banking_Supervision.ipynb): Explores the use of Giskard and its integration with FAID in an illustrative RAG application for banking supervision.

## Data Unit Tests and RAI Fields

- [data-unit-tests/demo-data-unit-tests.ipynb](data-unit-tests/demo-data-unit-tests.ipynb): Shows how to implement data unit tests for fairness.
- [rai-fields/demo-rai-logging.ipynb](rai-fields/demo-rai-logging.ipynb): Demonstrates using the RAI fields of other metadata formats.
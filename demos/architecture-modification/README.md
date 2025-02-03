# Adapter Fine Tuning

> #TODO: It is a work-in-progress. Integrate with FAID and demonstrate different approaches for adapter fine tuning. Demonstrate effectiveness of this approach as a bias mitigation technique.

**Adapter fine-tuning** is a technique used to modify and specialize pre-trained models like large language models (LLMs) without retraining the entire model. Instead of updating all the parameters, small, additional modules called **adapters** are inserted into the model. During training, only the adapters are updated, leaving the rest of the model's parameters frozen. This approach is computationally efficient and reduces the risk of overfitting.

To reduce bias, we can fine-tune adapters with bias-mitigated datasets or targeted interventions. For instance:

1. **Bias-Corrected Data**: Train the adapters using datasets curated to reduce stereotypical or biased patterns.
2. **Counterfactual Data Augmentation**: Use data with rewritten examples to address specific biases (e.g., gender, race).
3. **Regularization Techniques**: Apply constraints or loss functions to penalize biased outputs during fine-tuning.

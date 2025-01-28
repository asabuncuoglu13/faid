# Captum XAI library

> TODO: Explore other XAI libraries and techniques as a bias identification method.

**Link:** <https://captum.ai/>

Captum is an open-source library by PyTorch for model interpretability. It provides tools to analyse and visualise how ML models make predictions, helping understand which features contribute most to the output.

In this tutorial, we use *Integrated Gradients*. It is a method for attributing the output of a model (e.g., classification score) to its input features. It works by:
1. Creating a baseline input (e.g., all zeros or a neutral value).
2. Gradually interpolating between the baseline and the actual input.
3. Calculating the gradients of the model's output w.r.t. these interpolated inputs and integrating them over the path.

We can use this method for identifying bias to (a) see if protected characteristics disproportionately influence predictions, (b) modify sensitive attributes in inputs (e.g., changing "he" to "she") and observe if the attributions or outputs change significantly, and (c) identify systemic biases where certain features consistently dominate.

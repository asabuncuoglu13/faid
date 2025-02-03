# Responsible Development - Self Assessment

FAID (Fair AI Development) is an open-source fairness monitoring and management tool that developers can integrate into their machine learning (ML) pipelines. As the developers of FAID, it is also our shared responsibility to guide other developers on how to integrate FAID in a fairness by design approach.

## Bias and Discrimination Checklist

*The below list is adopted from EHRC <https://www.equalityhumanrights.com/guidance/artificial-intelligence-checklist-public-bodies-england>. You can also customise this checklist for integrating other open source software based on your needs.*

1. [ ] We know the meaning of the following protected characteristics and what are the implications of using them in the AI-enabled systems. (Protected attributes: Age, disability, gender reassignment, pregnancy and maternity (which includes breastfeeding), race, religion or belief, sex, sexual orientation.)
2. [ ] We identified if and how we (or others on your behalf) use the developed model, and considered how the regulations applies.
3. [ ] We collected necessary evidence to identify and address any research and implementation gaps that can cause a discriminative harm.
4. [ ] We reviewed how the AI could affect people with different protected characteristics either positively or negatively.
5. [ ] We assessed the potential and actual impact by looking at the equality evidence to evaluate if the AI model can potentially cause discrimination.
6. [ ] We assessed the potential and actual impact by looking at the equality evidence to evaluate if the AI model can potentially help eliminate discrimination.
7. [ ] We assessed the potential and actual impact by looking at the equality evidence to evaluate if the AI model can potentially contribute to advancing equality of opportunity.
8. [ ] We assessed the potential and actual impact by looking at the equality evidence to evaluate if the AI model can potentially affect good relations.
9. [ ] We used the results of the equality impact assessment when developing the AI-related features.
10. [ ] We recorded the fairness decisions and considerations throughout the development regularly.

*Below is taken from [fairlearn](https://fairlearn.org/main/user_guide/index.html)), which is originally published by Jacobs and Wallach, called “construct validity:” We can use it to detailly analyse if 4,5,6,7,8 are assured.*

1. [ ] Do the measurements produced by the model appear plausible on the surface?
2. [ ] Is there a single understanding of the theoretical construct, or is it contested and context-dependent?
3. [ ] Does the model contain the observable properties and related unobservable theoretical constructs specific to the construct of interest?
4. [ ] Does the model appropriately capture relationships between the construct of interest and the measured observable properties and related unobservable theoretical constructs?
5. [ ] Do the measurements obtained correlate with other established measurements for which construct validity has been established?
6. [ ] Do the measurements for the construct of interest correlate appropriately with related constructs?
7. [ ] Are the measurements obtained predictive of relevant observable properties or other unobservable theoretical constructs?
8. [ ] Are the hypotheses emerging from the measurements substantively interesting and relevant?
9. [ ] What are the societal impacts and consequences of using the measurements?
10. [ ] How is the world shaped by using the measurements, and what societal outcomes do we desire?

*And, below is taken from Ethics Guidelines for Trustworthy AI (EU High-Level Expert Group, 2019):*

1. [ ] We established a strategy or a set of procedures to avoid creating or reinforcing unfair bias in the AI system, both regarding the use of input data as well as for the algorithm design.
    - Did you assess and acknowledge the possible limitations stemming from the composition of the used data sets?
    - Did you consider diversity and representativeness of users in the data? Did you test for specific populations or problematic use cases?
    - Did you research and use available technical tools to improve your understanding of the data, model and performance?
    - Did you put in place processes to test and monitor for potential biases during the development, deployment and use phase of the system?

2. [ ] We ensured a mechanism that allows others to flag issues related to bias, discrimination or poor performance of the AI system.
    - Did you establish clear steps and ways of communicating on how and to whom such issues can be raised?
    - Did you consider others, potentially indirectly affected by the AI system, in addition to the (end)-users?
    - Did you assess whether there is any possible decision variability that can occur under the same conditions?
    - If so, did you consider what the possible causes of this could be?
    - In case of variability, did you establish a measurement or assessment mechanism of the potential impact of such variability on fundamental rights?

3. [ ] We ensured an adequate working definition of “fairness” that we apply in designing AI systems.
    - Is your definition commonly used? Did you consider other definitions before choosing this one?
    - Did you ensure a quantitative analysis or metrics to measure and test the applied definition of fairness?
    - Did you establish mechanisms to ensure fairness in your AI systems? Did you consider other potential mechanisms?

## Data Protection Checklist

*The below list is adopted from ICO <https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/accountability-and-governance/guide-to-accountability-and-governance>. You can also customise this checklist for integrating other open-source software based on your needs.*

- [ ] We thoroughly analyse the dataflow after integrating FAID to detect possible data protection issues as part of the design and implementation of our systems, services, products and business practices.
- [ ] We make data protection rules an essential component of the core functionality of our processing systems and services. We ensured that FAID is working under these rules.
- [ ] We included FAID into our risk register. We do not anticipate risks and privacy-invasive events due to this integration. We can identify possible risks before they occur and take steps to prevent harm to individuals.
- [ ] We only feed personal data to FAID that is needed for our purposes relating increasing fairness, and that we only use the data for those purposes.
- [ ] We ensure that any of FAID’s input and output personally identifiable data is automatically protected in any IT system.
- [ ] We reviewed and updated our data protection policy after the use of FAID  to provide individuals with tools so they can determine how we are using their personal data, and whether our policies are being properly enforced.
- [ ] When we use other systems, services or products in our processing activities, we make sure that we only use those whose designers and manufacturers take data protection issues into account.


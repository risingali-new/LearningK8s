# Session 25: Admission Control And Policy

This session teaches how clusters accept, reject, or mutate API requests.

## Sub-Session Order

1. `01-admission-flow`: authentication, authorization, admission.
2. `02-mutating-webhooks`: default or inject fields.
3. `03-validating-webhooks`: reject unsafe requests.
4. `04-kyverno`: policy-as-code with Kubernetes-native YAML.
5. `05-opa-gatekeeper`: Rego-based policy.
6. `06-policy-examples`: require labels, restrict images, block privileged Pods.
7. `07-policy-rollout`: audit first, enforce later.

## Review Questions

1. Where does admission happen in the API request flow?
2. What is the difference between mutation and validation?
3. Why should policy start in audit mode?
4. What kinds of mistakes can policy prevent?

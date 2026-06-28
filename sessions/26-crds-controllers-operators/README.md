# Session 26: CRDs, Controllers, And Operators

This session explains how Kubernetes is extended.

## Sub-Session Order

1. `01-crd-basics`: CustomResourceDefinition and CustomResource.
2. `02-controller-pattern`: watch, compare, reconcile.
3. `03-ownerreferences`: ownership and garbage collection.
4. `04-finalizers`: cleanup before deletion.
5. `05-status-subresource`: desired state versus observed state.
6. `06-operator-pattern`: encode operational knowledge.
7. `07-operator-examples`: cert-manager, Argo CD, External Secrets, VPA.

## Review Questions

1. What does a CRD add to the Kubernetes API?
2. What is reconciliation?
3. Why do controllers update status?
4. What problem do finalizers solve?

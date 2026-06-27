# Session 21: Helm

This session teaches Kubernetes packaging with Helm.

## Sub-Session Order

1. `01-helm-concepts`: chart, release, values, templates.
2. `02-install-a-chart`: install and inspect a release.
3. `03-create-a-chart`: package the sample app.
4. `04-values-files`: dev, stage, prod values.
5. `05-template-functions`: conditionals, loops, helpers.
6. `06-upgrade-and-rollback`: release lifecycle.
7. `07-chart-quality`: linting, schema, notes, chart testing.

## Useful Commands

```bash
helm repo add <name> <url>
helm install <release> <chart> -n <namespace> --create-namespace
helm upgrade <release> <chart> -f values.yaml
helm rollback <release> <revision>
helm template <release> <chart>
helm lint <chart>
```

## Review Questions

1. What is the difference between a chart and a release?
2. Why should values differ by environment?
3. What does `helm template` show?
4. When would you rollback a release?

# Introduction
This is a project to showcase how [Open Telemetry][otel] works in Python in a Kubernetes environment.

The project is structured as follows:

- `infra/`: Helm values according to release, cluster configuration and database.
- `apps/`: Kustomize manifests to deploy both applications.
- `src/`: Python source code of both applications. 

This environment can be quickly bootstrapped with k3d/k3s and Skaffold.

[otel]: https://opentelemetry.io/

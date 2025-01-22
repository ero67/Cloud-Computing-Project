# Infrastructure Validation Pipeline

This documentation outlines the Infrastructure Validation pipeline used to ensure the correctness of Kubernetes manifests in the `pipeline-project/k8s/` directory. The pipeline is triggered on specific events such as pushes to the `main` branch or pull requests, and can also be run manually.

## Workflow Triggers

The pipeline is triggered under the following conditions:
- **Manual Trigger**: The pipeline can be triggered manually using the `workflow_dispatch` event.
- **Push Event**: Triggered when changes are pushed to files in the `pipeline-project/k8s/` directory on the `main` branch.
- **Pull Request Event**: Triggered when a pull request involves changes to files in the `pipeline-project/k8s/` directory.

## Job: Validate

The pipeline consists of a single job named `validate`, which performs the following steps:

### 1. Checkout Code

Checks out the code from the repository to ensure the latest changes are available for validation.

```yaml
- name: Checkout code
  uses: actions/checkout@v2
```
### 2. Install kubeval
Installs `kubeval`, a tool used to validate Kubernetes configuration files.

```yaml
- name: Install kubeval
  run: |
    wget https://github.com/instrumenta/kubeval/releases/latest/download/kubeval-linux-amd64.tar.gz
    tar xf kubeval-linux-amd64.tar.gz
    sudo mv kubeval /usr/local/bin
```
### 3. Install kubeconform
Installs `kubeconform`, another tool for validating Kubernetes manifests, offering compatibility with Kubernetes schemas.

```yaml
- name: Install kubeconform
  run: |
    wget https://github.com/yannh/kubeconform/releases/latest/download/kubeconform-linux-amd64.tar.gz
    tar xf kubeconform-linux-amd64.tar.gz
    sudo mv kubeconform /usr/local/bin
```

### 4. Validate with kubeval
Validates the Kubernetes manifests using `kubeval` with strict mode and ignoring missing schemas.

```yaml
- name: Validate with kubeval
  run: |
    kubeval --strict --ignore-missing-schemas pipeline-project/k8s/base/[!kustomization]*.yaml
```

### 5. Validate with kubeconfrom
Validates the Kubernetes manifests using `kubeconform` with strict mode and ignoring missing schemas.
```yaml
- name: Validate with kubeconform
  run: |
    kubeconform -strict -ignore-missing-schemas pipeline-project/k8s/base/[!kustomization]*.yaml

```

## Conclusion

This pipeline ensures that all Kubernetes manifests in the `pipeline-project/k8s/` directory are validated for correctness using `kubeval` and `kubeconform`. These tools provide schema validation without requiring a live connection to a Kubernetes cluster, which makes the validation process more efficient and secure.

An alternative approach to validation could be using `kubectl apply --dry-run` to simulate the application of manifests without actually deploying them. However, this method requires a connection to a Kubernetes cluster, which could introduce unnecessary network dependencies and potential security concerns. By leveraging `kubeval` and `kubeconform`, we can perform thorough validation locally within the CI/CD pipeline, minimizing external dependencies and ensuring the validation process is isolated from the cluster environment.

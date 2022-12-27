# Dreambooth Container Tests
A repo to help documenent a containerized workflow for `Stable-Diffusion` + `Dreambooth` with AWS resources(e.g.: AWS ECR, AWS Batch).


## Docker Build Commands

```bash
# Build Dreambooth Image
docker build dreambooth -t dreambooth

# Build Pytourch Sandbox Image
docker build pytorchsandbox -t pytorchsandbox
```
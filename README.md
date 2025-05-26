# Block-Collector

A simple live blockchain block collection tool.

## Local Setup

`uv` is used for dependency management.
To begin with, after installing `uv`, run:

```bash
uv sync --all-extras
```

The data collection can be started using:

```bash
uv run start-collection
```

## GCP Setup

This tool can also be run on Google Cloud, with data being stored to GCP buckets.

1. Prepare you storage bucket:

```bash
gcloud storage buckets create gs://block-collector \
    --project=PROJECT-ID \
    --location=europe-west2 \
    --uniform-bucket-level-access
```

2. Source environment variables:

```bash
source .env
```

3. Spin up the VM:

```bash
gcloud compute instances create-with-container "$INSTANCE_NAME" \
  --project="$GCP_PROJECT_ID" \
  --zone=europe-west2-b \
  --machine-type=e2-micro \
  --boot-disk-size=20GB \
  --image-family=cos-stable \
  --image-project=cos-cloud \
  --scopes=https://www.googleapis.com/auth/cloud-platform \
  --container-image="$IMAGE_REFERENCE" \
  --container-restart-policy=always \
  --container-env=FLR_EXPLORER_URL="$FLR_EXPLORER_URL",\
SGB_EXPLORER_URL="$SGB_EXPLORER_URL",\
GCP_BUCKET_NAME="$GCP_BUCKET_NAME",\
GCP_PROJECT_ID="$GCP_PROJECT_ID"
```

## Analysis

To analyze collected data in JupyterLab, configure the kernel:

```bash
uv run python -m ipykernel install --user --name=block-collector
uv run jupyter lab
```

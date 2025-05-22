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
    --project=flare-network-sandbox \
    --location=europe-west2 \
    --uniform-bucket-level-access
```

2. Build and push the repository to Artifacts Registry (AR):

```bash
gcloud artifacts repositories create block-collector-repo \
  --project=flare-network-sandbox \
  --repository-format=docker \
  --location=europe-west2 \
  --description="Container images for block-collector"
```

3. Build and push directly to the AR repo:

```bash
gcloud builds submit \
  --tag europe-west2-docker.pkg.dev/flare-network-sandbox/block-collector-repo/block-collector:latest \
  .
```

4. Deploy and run (as a daemon):

```bash
gcloud run deploy block-collector \
  --image=europe-west2-docker.pkg.dev/flare-network-sandbox/block-collector-repo/block-collector:latest \
  --region=europe-west2 \
  --platform=managed \
  --allow-unauthenticated
```

5. Pin one instance (daemon mode) so your infinite loop stays alive:

```bash
gcloud run services update block-collector \
  --region=europe-west2 \
  --concurrency=1 \
  --min-instances=1 \
  --max-instances=1
```

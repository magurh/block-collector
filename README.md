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

2. Spin up the VM:

```bash
gcloud compute instances create block-collector-vm \
  --project=PROJECT-ID \
  --zone=europe-west2-b \
  --machine-type=e2-micro \
  --boot-disk-size=20GB \
  --image-family=debian-12 \
  --image-project=debian-cloud \
  --metadata startup-script='#! /bin/bash
apt-get update
apt-get install -y docker.io git
systemctl enable docker && systemctl start docker

# clone/build/run
git clone https://github.com/magurh/block-collector.git /opt/block-collector
docker build -t block-collector:latest /opt/block-collector
docker run -d \
  --name block-collector \
  --restart unless-stopped \
  -e GCS_BUCKET_NAME=block-collector \
  block-collector:latest'
```

#!/bin/sh

set -e

if [[ -z "$"{DATASTORE_PROJECT_ID} ]]; then
  echo "Missing DATASTORE_PROJECT_ID env variable"
  exit 1
fi

# Configure project
gcloud config set project ${DATASTORE_PROJECT_ID}

#start emulator

gcloud beta emulators datastore start \
  --consistency=1.0 \
  --host-port=0.0.0.0:8001 \
  --quiet \
  --data-dir /data

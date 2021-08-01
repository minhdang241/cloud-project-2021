#!/bin/bash
mkdir ~/.kube
echo $KUBE_CONFIG | base64 --decode - > ~/.kube/config
echo "NAMESPACE="$NAMESPACE > ./env/.env
echo $ENV_CONFIG | base64 --decode - >> ./env/.env
echo "KAFKA_PRODUCER_IMAGE="$KAFKA_PRODUCER_IMAGE >> ./env/.env 
echo "KAFKA_CONSUMER_IMAGE="$KAFKA_CONSUMER_IMAGE >> ./env/.env
echo "LABEL_STUDIO_IMPORTER_IMAGE="$LABEL_STUDIO_IMPORTER_IMAGE >> ./env/.env
echo "LABEL_STUDIO_EXPORTER_IMAGE="$LABEL_STUDIO_EXPORTER_IMAGE >> ./env/.env
echo "KUBEFLOW_PIPELINE_TRIGGER_IMAGE="$KUBEFLOW_PIPELINE_TRIGGER_IMAGE >> ./env/.env
echo "KUBEFLOW_INFERENCE_IMAGES="$KUBEFLOW_INFERENCE_IMAGES >> ./env/.env
python3 app/main.py
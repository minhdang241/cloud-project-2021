from kubernetes import client
from kubernetes.client.rest import ApiException

from app.resources import strings
from app.schemas.k8s.env import SampleEnvironment
from app.schemas.k8s.job import SampleJob
from ..core.config import settings


def create_transform_job_obj(data: SampleJob):
    """
    Function to create a transform job object

    Returns:
    - A V1Job object
    """

    envs = SampleEnvironment()

    # Create a list of V1EnvVar using the env_dict
    env_list = [client.V1EnvVar(name=key, value=value)
                for key, value in envs.dict().items()]

    # Configure Pod template container
    container = client.V1Container(
        name=data.container_name,
        image=settings.SAMPLE_IMAGE,
        image_pull_policy="Always",
        env=env_list,
    )

    # Create and configure a spec section
    pod_template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "sample-job"}),
        spec=client.V1PodSpec(restart_policy="OnFailure",
                              containers=[container]),
    )

    # Create the specification of deployment
    job_spec = client.V1JobSpec(
        template=pod_template,
        ttl_seconds_after_finished=100,  # Delete the completed job after 100 seconds
    )

    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(name=(data.job_name + str(data.job_id))),
        spec=job_spec,
    )

    return job


def create_job(job, *, namespace: str = strings.DEFAULT_NAMESPACE):
    """
    Function to run a job or cronjob

    Args:
        - api_instance: api object created using client
        - job: V1Job/V1beta1CronJob object
        - namespace: the namespace in which the job will be created

    Returns:
        - True if the object is created successfully otherwise False
    """
    try:
        if job.kind == "Job":
            client.BatchV1Api().create_namespaced_job(
                body=job, namespace=namespace)
        elif job.kind == "CronJob":
            client.BatchV1beta1Api().create_namespaced_cron_job(
                body=job, namespace=namespace
            )
        print("Job created")
        return True

    except ApiException as err:
        print(
            "Exception when calling BatchV1Api/BatchV1beta1Api->create_namespace_job: %s\n", err
        )
        return False

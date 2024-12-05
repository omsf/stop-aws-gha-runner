from moto import mock_aws
import boto3
from stop_aws_gha_runner.stop import StopAWS


@mock_aws
def test_remove_instance():
    ec2 = boto3.client("ec2", "us-west-2")
    response = ec2.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
    )
    ids = [response["Instances"][0]["InstanceId"]]
    StopAWS(region_name="us-west-2", instance_mapping={}).remove_instances(ids)
    status = ec2.describe_instance_status(InstanceIds=ids)
    assert (
        status["InstanceStatuses"][0]["InstanceState"]["Name"] == "terminated"
    )


@mock_aws
def test_wait_until_removed():
    region = "us-west-2"
    ec2 = boto3.client("ec2", region)
    response = ec2.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
    )
    ids = [response["Instances"][0]["InstanceId"]]
    stop_aws = StopAWS(region_name=region, instance_mapping={})
    stop_aws.remove_instances(ids)
    stop_aws.wait_until_removed(ids)


@mock_aws
def test_wait_until_removed_kwargs():
    region = "us-west-2"
    ec2 = boto3.client("ec2", region)
    response = ec2.run_instances(
        ImageId="ami-12345678",
        MinCount=1,
        MaxCount=1,
    )
    ids = [response["Instances"][0]["InstanceId"]]
    stop_aws = StopAWS(region_name=region, instance_mapping={})
    stop_aws.remove_instances(ids)
    kwargs = {"MaxAttempts": 2}
    stop_aws.wait_until_removed(ids, **kwargs)


def test_get_instance_mapping():
    instance_mapping = {"test": "mapping"}
    stop_aws = StopAWS(
        region_name="us-west-2", instance_mapping=instance_mapping
    )
    assert stop_aws.get_instance_mapping() == instance_mapping

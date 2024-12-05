from moto import mock_aws
import boto3
from stop_aws_gha_runner.stop import StopAWS
import pytest


@pytest.fixture(scope="function")
def aws():
    with mock_aws():
        region_name = "us-west-2"
        ec2 = boto3.client("ec2", region_name)
        response = ec2.run_instances(
            ImageId="ami-12345678",
            MinCount=1,
            MaxCount=1,
        )
        ids = [response["Instances"][0]["InstanceId"]]
        stop_aws = StopAWS(region_name=region_name, instance_mapping={})
        yield stop_aws, ids, ec2


def test_remove_instance(aws):
    stop_aws, ids, ec2 = aws
    stop_aws.remove_instances(ids)
    status = ec2.describe_instance_status(InstanceIds=ids)
    assert (
        status["InstanceStatuses"][0]["InstanceState"]["Name"] == "terminated"
    )


def test_wait_until_removed(aws):
    stop_aws, ids, ec2 = aws
    stop_aws.remove_instances(ids)
    stop_aws.wait_until_removed(ids)
    status = ec2.describe_instance_status(InstanceIds=ids)
    assert (
        status["InstanceStatuses"][0]["InstanceState"]["Name"] == "terminated"
    )


def test_wait_until_removed_kwargs(aws):
    stop_aws, ids, _ = aws
    stop_aws.remove_instances(ids)
    kwargs = {"MaxAttempts": 2}
    stop_aws.wait_until_removed(ids, **kwargs)


def test_get_instance_mapping():
    instance_mapping = {"test": "mapping"}
    stop_aws = StopAWS(
        region_name="us-west-2", instance_mapping=instance_mapping
    )
    assert stop_aws.get_instance_mapping() == instance_mapping

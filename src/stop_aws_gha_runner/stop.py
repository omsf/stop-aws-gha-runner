from dataclasses import dataclass
from gha_runner.clouddeployment import StopCloudInstance
import boto3


@dataclass
class StopAWS(StopCloudInstance):
    region_name: str
    instance_mapping: dict[str, str]

    def remove_instances(self, ids: list[str]):
        ec2 = boto3.client("ec2", self.region_name)
        params = {
            "InstanceIds": ids,
        }
        ec2.terminate_instances(**params)

    def wait_until_removed(self, ids: list[str], **kwargs):
        ec2 = boto3.client("ec2", self.region_name)
        waiter = ec2.get_waiter("instance_terminated")

        if kwargs:
            waiter.wait(InstanceIds=ids, WaiterConfig=kwargs)
        else:
            # Use a longer WaiterConfig to allow for GPU to properly terminate
            waiter_config = {"MaxAttempts": 80}
            waiter.wait(InstanceIds=ids, WaiterConfig=waiter_config)

    def get_instance_mapping(self) -> dict[str, str]:
        return self.instance_mapping

import os
from stop_aws_gha_runner.stop import StopAWS
from gha_runner.clouddeployment import TeardownInstance
from gha_runner.helper.input import EnvVarBuilder, check_required
from gha_runner.gh import GitHubInstance


def main():
    env = dict(os.environ)
    required = ["GH_PAT", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
    # Check for required environment variables
    check_required(env, required)
    # Build the environment variables

    builder = (
        EnvVarBuilder(env)
        # This is the default case
        .update_state("AWS_REGION", "region_name")
        # This is the input case
        .update_state("INPUT_AWS_REGION_NAME", "region_name")
        # This is the base case
        .update_state("GITHUB_REPOSITORY", "repo")
        # This is the input case
        .update_state("INPUT_GH_REPO", "repo")
        .update_state(
            "INPUT_INSTANCE_MAPPING", "instance_mapping", is_json=True
        )
    )

    token = os.environ["GH_PAT"]
    # This is not needed by the StopAWS class
    cloud_params = builder.params
    repo = cloud_params.pop("repo")

    gh = GitHubInstance(token, repo)
    deployment = TeardownInstance(StopAWS, cloud_params, gh)
    deployment = TeardownInstance(
        provider_type=StopAWS, cloud_params=cloud_params, gh=gh
    )
    deployment.stop_runner_instances()


if __name__ == "__main__":
    main()

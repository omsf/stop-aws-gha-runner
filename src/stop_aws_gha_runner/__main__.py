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
    aws_params = (
        EnvVarBuilder(env)
        # This is the default case
        .with_var("AWS_REGION", "region_name")
        # This is the input case
        .with_var("INPUT_AWS_REGION_NAME", "region_name")
        # This is the base case
        .with_var("GITHUB_REPOSITORY", "repo")
        # This is the input case
        .with_var("INPUT_GH_REPO", "repo")
        .with_var("INPUT_INSTANCE_MAPPING", "instance_mapping", is_json=True)
        .build()
    )

    token = os.environ["GH_PAT"]

    gh = GitHubInstance(token, repo=aws_params["repo"])
    deployment = TeardownInstance(StopAWS, cloud_params=aws_params, gh=gh)
    deployment.stop_runner_instances()


if __name__ == "__main__":
    main()

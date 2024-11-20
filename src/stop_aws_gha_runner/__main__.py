import os
from stop_aws_gha_runner.stop import StopAWS
from gha_runner.clouddeployment import TeardownInstance
from gha_runner.gh import GitHubInstance


def main():
    # Check for required environment variables
    required = ["GH_PAT", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
    for req in required:
        if req not in os.environ:
            raise Exception(f"Missing required environment variable {req}")
    aws_params = {}

    gha_params = {
        "token": os.environ["GH_PAT"],
    }
    repo = os.environ.get("INPUT_REPO")
    if repo is None or repo == "":
        repo = os.environ.get("GITHUB_REPOSITORY")
    # We check again to validate that this was set correctly
    if repo is not None or repo == "":
        gha_params["repo"] = repo
    else:
        raise Exception("Repo key is missing or GITHUB_REPOSITORY is missing")
    region_name = os.environ.get("INPUT_AWS_REGION_NAME")
    if region_name is not None:
        aws_params["region_name"] = region_name

    gh = GitHubInstance(token=os.environ["GH_PAT"], repo=gha_params["repo"])
    TeardownInstance(StopAWS, cloud_params=aws_params, gh=gh)


if __name__ == "__main__":
    main()

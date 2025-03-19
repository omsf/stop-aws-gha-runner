# stop-aws-gha-runner
This repository contains the code to stop a GitHub Actions runner on an AWS EC2 instance.
## Inputs
| Input             | Description                                                                                                                                                         | Required for stop| Default |
|-------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |----------------- |---------|
| instance_mapping  | A JSON object mapping instance ids to unique GitHub runner labels This should be the same as the AWS `start` output, `mapping`. Required to stop created instances. | true             |         |
| aws_region_name   | The AWS region name to use for your runner. Defaults to AWS_REGION                                                                                                  | true             | AWS_REGION |
| repo              | The repo to run against. Will use the current repo if not specified.                                                                                                | false            | The repo the runner is running in |
## Example usage
```yaml
name: Start and Stop AWS GHA Runner
on:
  workflow_run:
jobs:
  start-aws-runner:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    outputs:
      mapping: ${{ steps.aws-start.outputs.mapping }}
      instances: ${{ steps.aws-start.outputs.instances }}
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE }}
          aws-region: us-east-1
      - name: Create cloud runner
        id: aws-start
        uses: omsf/start-aws-gha-runner@v1.0.0
        with:
          aws_image_id: ami-0f7c4a792e3fb63c8
          aws_instance_type: g4dn.xlarge
          aws_home_dir: /home/ubuntu
        env:
          GH_PAT: ${{ secrets.GH_PAT }}
  stop-aws-runner:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    needs: start-aws-runner
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE }}
          aws-region: us-east-1
      - name: Stop cloud runner
        id: aws-stop
        uses: omsf/stop-aws-gha-runner@v1.0.0
        with:
          instance_mapping: ${{ needs.start-aws-runner.outputs.mapping }}
        env:
          GH_PAT: ${{ secrets.GH_PAT }}
```

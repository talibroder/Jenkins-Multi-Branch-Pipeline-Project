# Jenkins Multi-Branch Pipeline Project - Python Web-App Build, Test & Deployment to K8S Cluster.

## Overview

This *Jenkins Multi-Branch Pipeline* project automates the building, testing, and deployment for a *Python* web-app stored in a *GitLab* repository. The pipeline listens to push events on all repo branches distinguishing between the "main" branch and others. Two distinct workflows are implemented within one unified Jenkinsfile and are triggered based on the branch name. A versioning mechanism increments the appropriate segment of the app's versioning scheme according to the branch subject.


The project includes a **pre-commit script** that automates code quality, security, and compliance checks. Utilizes `git secrets`, `safety`, and `Trivy` for scanning. Enhances workflow efficiency and ensures code integrity. This pre-commit script runs in the local repo's `.git/hooks` folder for the pipeline versioning system to work properly.


The pipline connects to AWS S3 for retrieving the latest version tag listed as public bucket which contain txt file that specified the versioning. This is used by the versioning mechanism, ensuring the latest version is considered when incrementing the semantic version based on the branch name.


Upon successful re-build & testing of new updates in non-*main* branches, the pipeline automatically generates a merge request in the GitLab server. Push events and approved merge requests to *main* branch, trigger a deployment workflow, updating the Kubernetes cluster using a Helm chart stored in a separate Dockerhub repository.


The pipeline integrates with a Slack channel for real-time notifications.


## Prerequisites

### 1. Jenkins Configuration

- [Jenkins Server](https://www.jenkins.io/doc/book/installing/) installed and configured.
- [Jenkins agent configuration documentation](https://www.jenkins.io/doc/book/managing/distributed-builds/agent/)

### 2. GitLab Repository Configuration

- A GitLab repo on a private GitLab server with a "main" branch.
- A GitLab Integration configured to trigger the multibranch pipeline on the Jenkins server for *Push* and *Merge Request* events.

### 3. Kubernetes and Helm Configuration

- A Kubernetes cluster configured and accessible from the Jenkins server using a kube-config file.
- A Helm chart repository in Dockerhub for storing Helm packages for deployment.

### 4. Jenkins GitLab Connection

- A GitLab connection configured in Jenkins with a GitLab access token.

### 5. Jenkins Multibranch Pipeline Projects Configuration

- A *Multibranch Pipeline* project configured in Jenkins for the GitLab repository.

### 6. Slack channel Configured with a Jenkins app installed on it.

### 7. Jenkins Credentials Configuration

- **Credential ID: `dockerhub-token`**
  - Type: `Secret text`
  - Secret: `<Your DockerHub Access Token>`

- **Credential ID: `merge-request-token`**
  - Type: `Secret text`
  - Secret: `<Your GitLab Access Token>`

- **Credential ID: `kubectl_config`**
  - Type: `Secret file`
  - Secret File: `<Kubernetes Cluster Config File for remote access>`

- **Credential ID: `slack-token`**
  - Type: `Secret text`
  - Secret: `<Your Slack Channel API Token>`

### 7. Pipeline Environment Variable Configuration

- Pipeline environment variables set according to the user specific needs:
  - `IMG_NAME` - Name of your web-app Docker image.
  - `DOCKER_REPO` - Name of your Dockerhub repo (usually your user-name).
  - `HELM_REPO` - Name of your Dockerhub Helm chart repo (usually your user-name).
  - `GITLAB_HOST` - URL of your GitLab server (currenly http only)
  - `GIT_PROJECT_ID` - GitLab project ID

### 8. Save Pre-commit Script
  - Save the *pre-commit* script in the local repo `.git/hooks` folder for the pipeline versioning system to work properly.


## Pipeline Workflow

1. **Branch Detection:**
   - Jenkins listens for push events on all branches, distinguishing between "main" and others.

2. **Docker Image Build:**
   - For non-*main* branches, pipeline builds an updated Docker image of the Python web-app.

3. **Regression Testing:**
   - For non-*main* branches, pipeline Runs regression tests using Selenium and Integration test using unit-test moudle.

4. **Push to DockerHub:**
   - For non-*main* branches, uppon successful builds and tests the pipeline increments version scheme based on branch name and pushes the updated Docker image to DockerHub with ne version tag.
   *(Patch increment for "Fix" branches and minor increment for "Feature" branches)*

5. **Create Merge Request:**
   - For non-*main* branches, pipeline then generates a merge request to main branch.

6. **Update K8S Cluster:**
   - For the *main* branch, pipeline updates the Kubernetes cluster using the Helm chart.



## Usage

1. Configure Jenkins server with required plugins.
2. Set up Jenkins agent with Helm, kubectl, and Docker pre-installed.
3. Set up GitLab repository on a private GitLab server with main branch and a Integration configured.
4. Set up Jenkins multibranch pipeline project for the GitLab repository.
5. Configure GitLab connection in Jenkins with a GitLab access token.
6. Configure Jenkins credentials manager with all necessary credentials.
7. Set pipeline environment variables in Jenkinsfile according to the user's specific needs.
8. Save the pre-commit script in the local `.git/hooks` folder.
9. Run the pipeline manually or let it trigger automatically on push events to *main*, *Fix* or *Feature* branches.

## Notes

Feel free to enhance or customize this pipeline according to your specific needs. Happy automating!

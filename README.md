# PRetty-autotests



## Getting started

Need setup next files - config, framework



## Framework Setup on local machine
    1. Enable two-factor authentication
        a. Goto git
        b. Click on your profile avatar
        c. Click on edit profile 
        d. Click on Account
        e. Enable to two-facto authentication
    2. Configure Oauth using instruction mentioned in  https://docs.gitlab.com/integration/oauth_provider/ ( redirect URI is http://127.0.0.1/ ) and copy application id and secret code.
    3. Clear any old configuration (if required) using executing below commands on terminal
        a. git config --global --unset-all credential.https://git.andersenlab.com.gitLabDevClientId
        b.  git config --global --unset-all credential.https://git.andersenlab.com.gitLabDevClientSecret
        c. git config --global --unset-all credential.https://git.andersenlab.com.provider
    4. Now, configure the setup by running below commands on terminal.
        a. git config --global credential.https://git.andersenlab.com.gitLabDevClientId <application id>
        b. git config --global credential.https://git.andersenlab.com.gitLabDevClientSecret <secret code>
    5. Clone the Pretty-autotests repository using below command on terminal
        a. git clone <repository url>

## Requirements:
* Python 3.11, NOT lower.
* Install Poetry - pip install poetry
* Setup requirements - poetry install
* Install required browsers for playwright - playwright install
* Activation pre-commit - pre-commit install


## Run tests:
* Run one test: "pytest tests/<module_name>/<test_name>"
* Run all tests: "pytest tests/"
* Run using pytest-xdist: "pytest -n <n>"


## Add your files

- push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.andersenlab.com/Andersen/pretty_2.0/pretty-autotests.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.andersenlab.com/Andersen/pretty_2.0/pretty-autotests/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing (SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***




## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.

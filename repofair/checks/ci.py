import os
import glob


def check_ci(repo_path: str) -> dict:
    """Check for CI/CD configuration. Maps to FAIR: Accessible."""
    workflows_dir = os.path.join(repo_path, ".github", "workflows")
    if os.path.isdir(workflows_dir):
        workflows = (
            glob.glob(os.path.join(workflows_dir, "*.yml"))
            + glob.glob(os.path.join(workflows_dir, "*.yaml"))
        )
        if workflows:
            count = len(workflows)
            return {
                "check": "CI/CD",
                "fair": "A",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"GitHub Actions: {count} workflow(s) found",
            }

    other_ci = [
        ".travis.yml",
        "Jenkinsfile",
        ".gitlab-ci.yml",
        ".circleci/config.yml",
        "azure-pipelines.yml",
        ".drone.yml",
        "bitbucket-pipelines.yml",
    ]
    for ci_file in other_ci:
        if os.path.exists(os.path.join(repo_path, ci_file)):
            return {
                "check": "CI/CD",
                "fair": "A",
                "passed": True,
                "score": 10,
                "max_score": 10,
                "message": f"{ci_file} found",
            }

    return {
        "check": "CI/CD",
        "fair": "A",
        "passed": False,
        "score": 0,
        "max_score": 10,
        "message": "No CI/CD configuration found",
    }

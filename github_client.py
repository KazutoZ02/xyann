import asyncio
from typing import Dict, Any, Optional
import config
from github import Github, GithubException

class GitHubClient:
    """Async wrapper around PyGithub for repository management and code commits."""

    def __init__(self, token: Optional[str] = None):
        self.token = token or config.GITHUB_TOKEN

    def _get_gh_instance(self) -> Github:
        if not self.token:
            raise ValueError("GITHUB_TOKEN is missing in environment variables.")
        return Github(self.token)

    async def create_repository(
        self,
        name: str,
        description: str = "Created via Antigravity NVIDIA Discord AI Bot",
        private: bool = False
    ) -> Dict[str, Any]:
        """Creates a new GitHub repository for the authenticated user."""
        def _sync_create():
            gh = self._get_gh_instance()
            user = gh.get_user()
            repo = user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=True  # Creates initial README.md
            )
            return {
                "name": repo.name,
                "full_name": repo.full_name,
                "html_url": repo.html_url,
                "clone_url": repo.clone_url,
                "private": repo.private
            }

        try:
            repo_info = await asyncio.to_thread(_sync_create)
            return {"success": True, "repo": repo_info}
        except GithubException as e:
            return {"success": False, "error": f"GitHub API Error: {e.data.get('message', str(e))}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to create repo: {str(e)}"}

    async def push_code_file(
        self,
        repo_name: str,
        file_path: str,
        content: str,
        commit_message: str = "Add code file via Antigravity Discord AI",
        branch: str = "main"
    ) -> Dict[str, Any]:
        """Creates or updates a file in a specified GitHub repository."""
        def _sync_push():
            gh = self._get_gh_instance()
            user = gh.get_user()
            
            # If repo_name doesn't include owner (user/repo), prepend user's login
            target_name = repo_name if "/" in repo_name else f"{user.login}/{repo_name}"
            repo = gh.get_repo(target_name)
            
            try:
                # Try getting existing file to update
                existing_file = repo.get_contents(file_path, ref=branch)
                res = repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha,
                    branch=branch
                )
                action = "updated"
            except GithubException:
                # File doesn't exist, create new file
                res = repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    branch=branch
                )
                action = "created"

            commit = res["commit"]
            content_file = res["content"]
            return {
                "action": action,
                "file_path": content_file.path,
                "file_url": content_file.html_url,
                "commit_sha": commit.sha[:7],
                "commit_url": commit.html_url,
                "repo_url": repo.html_url
            }

        try:
            res_info = await asyncio.to_thread(_sync_push)
            return {"success": True, "details": res_info}
        except GithubException as e:
            return {"success": False, "error": f"GitHub Commit Error: {e.data.get('message', str(e))}"}
        except Exception as e:
            return {"success": False, "error": f"Failed to push code: {str(e)}"}

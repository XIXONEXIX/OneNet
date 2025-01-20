import subprocess
import os

def run_git_command(command, cwd):
    """Runs a git command and returns the output."""
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return result.stdout, result.stderr

def git_sync(repo_dir):
    # Change to the repository directory
    os.chdir(repo_dir)
    print(f"Changing directory to {repo_dir}")
    
    # Fetch the latest changes from the remote
    print("Fetching latest changes from the remote...")
    fetch_stdout, fetch_stderr = run_git_command(["git", "fetch"], cwd=repo_dir)
    print(fetch_stdout)
    if fetch_stderr:
        print(f"Error: {fetch_stderr}")

    # Check for local changes
    print("Checking for local changes...")
    status_stdout, status_stderr = run_git_command(["git", "status"], cwd=repo_dir)
    print(status_stdout)
    
    if "nothing to commit" in status_stdout:  # No changes detected
        print("No local changes to commit.")
    else:
        # Add untracked files and commit changes
        print("Local changes detected. Adding and committing...")
        run_git_command(["git", "add", "."], cwd=repo_dir)
        commit_stdout, commit_stderr = run_git_command(["git", "commit", "-m", "Sync changes"], cwd=repo_dir)
        print(commit_stdout)
        if commit_stderr:
            print(f"Error: {commit_stderr}")
        
        # Push changes to the remote repository
        print("Pushing changes to the remote branch main...")
        push_stdout, push_stderr = run_git_command(["git", "push", "origin", "main", "--force"], cwd=repo_dir)
        print(push_stdout)
        if push_stderr:
            print(f"Error: {push_stderr}")

if __name__ == "__main__":
    repo_dir = "D:\\OneNet"  # Set the path to your repository
    git_sync(repo_dir)

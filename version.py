# version.py
import subprocess


def get_version_from_github():
    try:
        # Get short commit hash
        commit = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode().strip()

        # Try to get the latest tag
        try:
            tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev=0']).decode().strip()
        except subprocess.CalledProcessError:
            # No tags found, use default
            tag = "v1.0.0"

        return f"{tag} ({commit})"

    except subprocess.CalledProcessError:
        # Not in a git repository or git not available
        return "v1.0.0 (unknown)"


def print_version():
    version = get_version_from_github()
    print(f"Version: {version}")
    return version


if __name__ == "__main__":
    print_version()
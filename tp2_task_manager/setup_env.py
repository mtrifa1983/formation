"""
Setup script to create Python virtual environment and install dependencies.

Run this script to set up the project environment:
    python setup_env.py
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """
    Run a shell command and report success/failure.
    
    Args:
        command: The command to run.
        description: Description of what the command does.
        
    Returns:
        True if successful, False otherwise.
    """
    print(f"\n{'=' * 60}")
    print(f"Setting up: {description}")
    print(f"{'=' * 60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True)
        print(f"✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"✗ {description} failed: {str(e)}")
        return False


def setup_environment() -> None:
    """Set up the project environment."""
    print("\n" + "=" * 60)
    print("TASK MANAGER - ENVIRONMENT SETUP")
    print("=" * 60)
    
    # Get project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    success = True
    
    # Create virtual environment
    venv_path = project_dir / "venv"
    if not venv_path.exists():
        success &= run_command(
            f"{sys.executable} -m venv venv",
            "Creating Python virtual environment"
        )
    else:
        print("✓ Virtual environment already exists at ./venv")
    
    # Determine the pip command based on OS
    if sys.platform == "win32":
        pip_cmd = ".\\venv\\Scripts\\pip"
        python_cmd = ".\\venv\\Scripts\\python"
    else:
        pip_cmd = "./venv/bin/pip"
        python_cmd = "./venv/bin/python"
    
    # Upgrade pip
    success &= run_command(
        f"{pip_cmd} install --upgrade pip",
        "Upgrading pip"
    )
    
    # Install requirements
    if (project_dir / "requirements.txt").exists():
        success &= run_command(
            f"{pip_cmd} install -r requirements.txt",
            "Installing project dependencies"
        )
    else:
        print("⚠ requirements.txt not found, skipping dependency installation")
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✓ SETUP COMPLETED SUCCESSFULLY!")
        print("\nNext steps:")
        if sys.platform == "win32":
            print("1. Activate virtual environment: .\\venv\\Scripts\\activate")
        else:
            print("1. Activate virtual environment: source venv/bin/activate")
        print("2. Run the application: python app.py")
        print("3. Run tests: python test_app.py")
    else:
        print("✗ SETUP COMPLETED WITH ERRORS")
        print("Please check the output above for details.")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    setup_environment()

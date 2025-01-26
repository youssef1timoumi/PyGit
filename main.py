from git import Repo, GitCommandError
import os
import pandas as pd
from datetime import datetime

# Repository settings
GITHUB_REPO_URL = "your-github-repo-url-here (SSH required)"  # Replace with your SSH URL
LOCAL_REPO_PATH = "your-local-repo-path"  # Path to clone the repository


# Clone or pull the repository
def setup_repo():
    try:
        if not os.path.exists(LOCAL_REPO_PATH):
            print("Cloning repository...")
            Repo.clone_from(GITHUB_REPO_URL, LOCAL_REPO_PATH)
        else:
            print("Pulling latest changes...")
            repo = Repo(LOCAL_REPO_PATH)
            repo.remotes.origin.pull()
    except GitCommandError as e:
        print(f"Error while setting up the repository: {e}")


# Commit and push changes
def push_changes(commit_message):
    try:
        repo = Repo(LOCAL_REPO_PATH)
        if repo.is_dirty():
            repo.git.add(A=True)  # Stage all changes
            repo.index.commit(commit_message)
            repo.remotes.origin.push()
            print("Changes pushed to GitHub!")
        else:
            print("No changes to push.")
    except GitCommandError as e:
        print(f"Error while pushing changes: {e}")


# Append data to an Excel file
def append_to_excel(file_name, new_row_data):
    file_path = os.path.join(LOCAL_REPO_PATH, file_name)

    try:
        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
        else:
            print(f"{file_name} not found. Creating a new one.")
            df = pd.DataFrame(columns=new_row_data.keys())

        new_row_df = pd.DataFrame([new_row_data])  # Create a DataFrame for the new row
        df = pd.concat([df, new_row_df], ignore_index=True)

        df.to_excel(file_path, index=False)
        print(f"Data saved to {file_name}!")
    except Exception as e:
        print(f"Error while appending to {file_name}: {str(e)}")


# Example data input and usage
def main():
    setup_repo()
    print("Choose an operation:")
    print("1: Add example data to Excel file")
    print("2: Calculate total from a column in an Excel file")

    choice = int(input("Enter your choice: "))
    if choice == 1:
        example_data = {
            "Name": "John Doe",
            "Description": "Example data entry",
            "Amount": 100.0,
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        append_to_excel("example_data.xlsx", example_data)
        push_changes("Added example data on " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    elif choice == 2:
        file_name = "example_data.xlsx"
        column_name = "Amount"
        file_path = os.path.join(LOCAL_REPO_PATH, file_name)

        if os.path.exists(file_path):
            df = pd.read_excel(file_path)
            total = df[column_name].sum()
            print(f"Total of column '{column_name}': {total}")
        else:
            print(f"{file_name} not found.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()

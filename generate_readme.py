import os
import re

def extract_number(filename):
    """Extract numbers from filenames for sorting."""
    match = re.search(r"(\d+\.\d+|\d+)", filename)
    return float(match.group(1)) if match else float('inf')

def generate_markdown_link(path, base_url):
    """Generate GitHub markdown link for a given file path."""
    readable_path = path.replace(' ', '%20').replace('./', '')
    return f"[{os.path.basename(path)}]({base_url}{readable_path})"

def list_files(directory, base_url, prefix=""):
    """Recursively list files in directory, generating markdown links."""
    entries = os.listdir(directory)
    entries.sort(key=extract_number)
    markdown_content = ""
    ignore_files = {'.git', 'generate_readme.py', 'README.md'}

    for item in entries:
        if item.startswith('.') or item in ignore_files:
            continue

        full_path = os.path.join(directory, item)
        if os.path.isdir(full_path):
            markdown_content += f"{prefix}- {item}\n"  # Remove the slash for directories
            markdown_content += list_files(full_path, base_url, prefix + "    ")
        else:
            markdown_content += f"{prefix}- {generate_markdown_link(full_path, base_url)}\n"
    return markdown_content

def update_readme_section(readme_path, new_content, start_marker, end_marker):
    """Update only a specific section of the README.md file."""
    with open(readme_path, 'r+') as file:
        content = file.read()
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)

        if start_index < len(start_marker) or end_index == -1:
            raise ValueError("Start or end marker not found in README file.")

        updated_content = content[:start_index] + "\n" + new_content + "\n" + content[end_index:]
        file.seek(0)
        file.write(updated_content)
        file.truncate()

# Configuration
base_url = "https://github.com/e-juhee/react-deep-dive/blob/main/"
directory_path = './'  # Adjust as needed
readme_path = 'README.md'  # Path to the README file
start_marker = "<!-- FOLDER_STRUCTURE_START -->"
end_marker = "<!-- FOLDER_STRUCTURE_END -->"

# Generate folder structure and update README.md
folder_structure = list_files(directory_path, base_url)
print(folder_structure)
update_readme_section(readme_path, folder_structure, start_marker, end_marker)

import os
import glob

def search_document(query, search_path="."):
    extensions = ["*.pdf", "*.docx", "*.txt"]
    matching_files = []

    # Search in all directories from the given path
    for ext in extensions:
        matching_files.extend(glob.glob(os.path.join(search_path, "**", ext), recursive=True))

    # Filter files based on the query (file name)
    query_lower = query.lower()
    result_files = [file for file in matching_files if query_lower in os.path.basename(file).lower()]
    
    if result_files:
        return result_files[0]  # Return the first match
    return None

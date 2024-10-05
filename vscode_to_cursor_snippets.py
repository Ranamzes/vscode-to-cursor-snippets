import hjson
import json
import os
import platform
import sys

def get_paths():
    system = platform.system()
    home = os.path.expanduser("~")
    
    if system == "Windows":
        vscode_path = os.path.join(home, "AppData", "Roaming", "Code", "User", "snippets")
        cursor_path = os.path.join(home, "AppData", "Roaming", "cursor", "User", "snippets")
    elif system == "Darwin":  # macOS
        vscode_path = os.path.join(home, "Library", "Application Support", "Code", "User", "snippets")
        cursor_path = os.path.join(home, "Library", "Application Support", "cursor", "User", "snippets")
    elif system == "Linux":
        vscode_path = os.path.join(home, ".config", "Code", "User", "snippets")
        cursor_path = os.path.join(home, ".config", "cursor", "User", "snippets")
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)
    
    return vscode_path, cursor_path

def convert_snippets(snippets):
    result = {}
    for name, snippet in snippets.items():
        result[name] = {
            "prefix": snippet.get("prefix", ""),
            "body": snippet.get("body", []) if isinstance(snippet.get("body"), list) else [snippet.get("body", "")],
            "description": snippet.get("description", "")
        }
    return result

def main():
    vscode_snippets_path, cursor_snippets_path = get_paths()

    print(f"VSCode snippets path: {vscode_snippets_path}")
    print(f"Cursor snippets path: {cursor_snippets_path}")

    # Create the Cursor snippets directory if it doesn't exist
    os.makedirs(cursor_snippets_path, exist_ok=True)

    # Process all VSCode snippet files
    for filename in os.listdir(vscode_snippets_path):
        if filename.endswith(".json"):
            vscode_file_path = os.path.join(vscode_snippets_path, filename)
            cursor_file_path = os.path.join(cursor_snippets_path, filename)
            try:
                with open(vscode_file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Parse the file content using hjson
                vscode_snippets = hjson.loads(content)
                
                # Convert snippets to Cursor format
                cursor_snippets = convert_snippets(vscode_snippets)
                
                # Save snippets in Cursor format
                with open(cursor_file_path, "w", encoding="utf-8") as f:
                    json.dump(cursor_snippets, f, indent=2, ensure_ascii=False)
                
                print(f"Successfully processed file: {filename}")
                print(f"  Source file: {vscode_file_path}")
                print(f"  New file: {cursor_file_path}")
                print(f"  Number of snippets: {len(cursor_snippets)}")
            except Exception as e:
                print(f"Error processing file {filename}:")
                print(f"  {str(e)}")
                print(f"  Please check the file content manually: {vscode_file_path}")

    print("Processing completed.")

if __name__ == "__main__":
    main()
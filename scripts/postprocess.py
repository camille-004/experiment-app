import os

def postprocess_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace("\n{%", "{%")
    content = content.replace("%}\n", "%}")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def main():
    for root, _, files in os.walk('frontend/templates'):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                postprocess_file(file_path)

if __name__ == "__main__":
    main()

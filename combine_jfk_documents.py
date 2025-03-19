import os

# Input text files
under_1mb_file = "jfk_documents_under_1mb.txt"
over_1mb_file = "jfk_documents_over_1mb.txt"

# Output combined text file
combined_file = "jfk_documents_combined.txt"

# Dictionary to store documents (filename: content)
documents = {}

# Read the under 1 MB file
if os.path.exists(under_1mb_file):
    with open(under_1mb_file, 'r', encoding='utf-8') as f:
        current_doc = None
        content = []
        for line in f:
            if line.startswith("Document: "):
                if current_doc:  # Save the previous document
                    documents[current_doc] = ''.join(content)
                current_doc = line.split("Document: ")[1].strip()
                content = [line]
            else:
                content.append(line)
        if current_doc:  # Save the last document
            documents[current_doc] = ''.join(content)

# Read the over 1 MB file
if os.path.exists(over_1mb_file):
    with open(over_1mb_file, 'r', encoding='utf-8') as f:
        current_doc = None
        content = []
        for line in f:
            if line.startswith("Document: "):
                if current_doc:  # Save the previous document
                    documents[current_doc] = ''.join(content)
                current_doc = line.split("Document: ")[1].strip()
                content = [line]
            else:
                content.append(line)
        if current_doc:  # Save the last document
            documents[current_doc] = ''.join(content)

# Write combined file in sorted order
try:
    with open(combined_file, 'w', encoding='utf-8') as f:
        for filename in sorted(documents.keys()):
            f.write(documents[filename])
    print(f"Combined text files into {combined_file}")
except Exception as e:
    print(f"Error combining text files: {e}")
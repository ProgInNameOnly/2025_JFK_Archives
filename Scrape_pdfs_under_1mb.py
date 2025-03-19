import os
import PyPDF2
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import time

# Directory containing the PDFs
pdf_dir = "JFK_PDFs"

# Output text file for PDFs under 1 MB
output_text_file = "jfk_documents_under_1mb.txt"

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Add Poppler to PATH
os.environ["PATH"] += os.pathsep + r"C:\Users\tdent\Desktop\JFK\poppler-24.08.0\Library\bin"

# Counter for processed files
count = 0

# Set to keep track of processed files
processed_files = set()

# Load already processed files from the output text file
if os.path.exists(output_text_file):
    with open(output_text_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith("Document: "):
                filename = line.split("Document: ")[1].strip()
                processed_files.add(filename)

try:
    # Open the output text file in append mode
    with open(output_text_file, 'a', encoding='utf-8') as text_file:
        # Iterate through all files in the PDF directory
        for filename in sorted(os.listdir(pdf_dir)):
            if filename.lower().endswith('.pdf') and os.path.isfile(os.path.join(pdf_dir, filename)):
                # Get file size in bytes
                file_path = os.path.join(pdf_dir, filename)
                file_size = os.path.getsize(file_path)

                # Process only files under 1 MB (1,048,576 bytes)
                if file_size >= 1048576:  # 1 MB
                    print(f"Skipping {filename} (size: {file_size / 1048576:.2f} MB) - over 1 MB")
                    continue

                # Skip already processed files
                if filename in processed_files:
                    print(f"Skipping already processed file: {filename}")
                    count += 1
                    continue

                try:
                    # Step 1: Try PyPDF2 for text-based PDFs
                    text = ""
                    with open(file_path, 'rb') as pdf_file:
                        pdf_reader = PyPDF2.PdfReader(pdf_file)
                        for page_num, page in enumerate(pdf_reader.pages, 1):
                            page_text = page.extract_text()
                            if page_text:
                                text += f"Page {page_num}:\n{page_text}\n\n"

                    # Step 2: If no text found, use OCR with timeout
                    if not text.strip():
                        print(f"No text found in {filename} with PyPDF2; attempting OCR...")
                        start_time = time.time()
                        timeout = 30  # 30 seconds timeout per file
                        images = None
                        try:
                            images = convert_from_path(file_path)
                        except Exception as e:
                            print(f"Error converting PDF to images: {e}")
                            text = "Error during image conversion.\n"
                        if images:
                            for i, image in enumerate(images):
                                try:
                                    ocr_text = pytesseract.image_to_string(image, timeout=10)  # 10 seconds per page
                                    text += f"Page {i+1}:\n{ocr_text}\n\n"
                                except Exception as e:
                                    text += f"Page {i+1}: OCR timeout or error: {e}\n\n"
                            del images  # Free memory

                    # Write document header and text to file
                    text_file.write(f"\n{'='*50}\n")
                    text_file.write(f"Document: {filename}\n")
                    text_file.write(f"{'='*50}\n")
                    text_file.write(text if text.strip() else "No extractable text found after OCR.\n")
                    
                    count += 1
                    print(f"Processed: {filename} (size: {file_size / 1048576:.2f} MB)")

                except Exception as e:
                    text_file.write(f"\n{'='*50}\n")
                    text_file.write(f"Document: {filename}\n")
                    text_file.write(f"{'='*50}\n")
                    text_file.write(f"Error processing: {str(e)}\n")
                    print(f"Error processing {filename}: {e}")
                    count += 1

    print(f"Completed. Processed {count} PDFs under 1 MB. Text dumped to {output_text_file}")

except Exception as e:
    print(f"Error writing to text file: {e}")
import os
import plistlib
import hashlib

def extract_and_generate_markdown(webarchive_path, output_dir, markdown_file_path):
    with open(webarchive_path, 'rb') as file:
        webarchive_data = plistlib.load(file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(markdown_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write("# Extracted Images\n\n")

        for resource in webarchive_data.get('WebSubresources', []):
            url = resource.get('WebResourceURL', 'unknown')
            mime_type = resource.get('WebResourceMIMEType', 'unknown')
            data = resource.get('WebResourceData', b'')

            # Use the URL to determine the filename
            filename = os.path.basename(url)
            if not filename:
                # Generate a filename if the URL doesn't provide one
                filename = hashlib.md5(url.encode()).hexdigest()

            # Save the image if it's an image type
            if mime_type.startswith('image/'):
                image_path = os.path.join(output_dir, filename)
                with open(image_path, 'wb') as img_file:
                    img_file.write(data)

                # Write a Markdown link to the image
                md_file.write(f"![{filename}]({filename})\n\n")

    print(f"Markdown file generated at {markdown_file_path}")

if __name__ == "__main__":
    webarchive_path = '/Users/ang/Desktop/jj/JamesFriends.webarchive'
    output_directory = '/Users/ang/Desktop/jj/ExtractedImages'
    markdown_file_path = '/Users/ang/Desktop/jj/extracted_images.md'

    extract_and_generate_markdown(webarchive_path, output_directory, markdown_file_path)
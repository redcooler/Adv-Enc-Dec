import re

def extract_emails(text):
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    return re.findall(email_pattern, text)

def extract_ips(text):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    return re.findall(ip_pattern, text)

def extract_urls(text):
    url_pattern = r'https?://[^\s"]+'
    return re.findall(url_pattern, text)

def extract_phone_numbers(text):
    phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_pattern, text)

def extract_from_file(filepath):
    """
    Extract all supported data types from a file, only if it can be read as plaintext.
    Returns a dict of results, or None if the file is not plaintext.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        print(f"File '{filepath}' is not a plaintext (UTF-8) file. Skipping.")
        return None
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        return None

    return {
        "emails": extract_emails(text),
        "ips": extract_ips(text),
        "urls": extract_urls(text),
        "phone_numbers": extract_phone_numbers(text)
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract emails, IPs, URLs, and phone numbers from a plaintext file.")
    parser.add_argument("file", help="Path to the file to extract data from")
    args = parser.parse_args()

    results = extract_from_file(args.file)
    if results is None:
        print("No data extracted (file may not be plaintext).")
    else:
        for key, values in results.items():
            print(f"\n{key.capitalize()}:")
            for value in values:
                print(f"  {value}")

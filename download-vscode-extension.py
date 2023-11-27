import argparse
import requests
import os
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Referer': 'https://marketplace.visualstudio.com/items?itemName=ms-python.python',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'TE': 'trailers'
}

# Updated cookies
cookies = {
    'VstsSession': '%7B%22PersistentSessionId%22%3A%224550fe5a-845e-4701-904a-abc628dc754a%22%2C%22PendingAuthenticationSessionId%22%3A%2200000000-0000-0000-0000-000000000000%22%2C%22CurrentAuthenticationSessionId%22%3A%2200000000-0000-0000-0000-000000000000%22%2C%22SignInState%22%3A%7B%7D%7D',
    'Gallery-Service-UserIdentifier': '9e61b919-76d5-404a-abb7-4f9a7266d379',
    'Market_SelectedTab': 'vscode'
}
def get_latest_version(extension_id):
    url = f"https://marketplace.visualstudio.com/items?itemName={extension_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Use regex to find the version number in the page content
        match = re.search(r'"version":"([\d.]+)"', response.text)
        if match:
            return match.group(1)
    return None

def download_extension(extension_id, save_path):
    # Fetch the latest version number for the extension
    version = get_latest_version(extension_id)
    if not version:
        print(f"Could not find version for {extension_id}")
        return

    # Extract publisher and extension name from the ID
    publisher, extension_name = extension_id.split('.')

    # Construct download URL for the .vsix file
    download_url = f"https://marketplace.visualstudio.com/_apis/public/gallery/publishers/{publisher}/vsextensions/{extension_name}/{version}/vspackage"
    
    print("Download URL: "+download_url)
    # Download the extension
    vsix_response = requests.get(download_url, headers=headers, cookies=cookies)
    print("VSIX Responde: "+str(vsix_response.status_code))
    if vsix_response.status_code == 200:
        with open(os.path.join(save_path, f"{extension_id}-{version}.vsix"), 'wb') as file:
            file.write(vsix_response.content)
        print(f"Downloaded {extension_id} version {version}")
    else:
        print(f"Failed to download {extension_id} version {version}")

def main():
    parser = argparse.ArgumentParser(description='Download VSCode extensions.')
    parser.add_argument('--extension', help='Extension ID to download')
    parser.add_argument('--file', help='File containing list of extensions')
    args = parser.parse_args()
    
    save_path = './vscode-extensions'

    # Check if the directory exists, if not, create it
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if args.extension:
        download_extension(args.extension, save_path)
    elif args.file:
        with open(args.file, 'r') as file:
            for line in file:
                extension_id = line.strip()
                download_extension(extension_id, save_path)

if __name__ == "__main__":
    main()

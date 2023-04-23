import argparse
import requests
import re
from termcolor import colored

def find_subdomains(domain):
    subdomains = set()

    # Subdomain enumeration using Certificate Transparency logs
    ct_url = 'https://crt.sh/?q=%.{d}&output=json'
    r = requests.get(ct_url.format(d=domain))
    if r.ok:
        for cert in r.json():
            subdomains.add(cert['name_value'].lower())

    # Subdomain enumeration using DNS queries
    dns_servers = ['8.8.8.8', '1.1.1.1']  # Google and Cloudflare DNS servers
    for dns_server in dns_servers:
        try:
            answers = dns.resolver.query(domain, 'A', dns_server)
            for answer in answers:
                subdomains.add(str(answer).lower())
        except:
            pass

    # Subdomain enumeration using web scraping
    url = f'http://www.ask.com/web?q={domain}'
    r = requests.get(url)
    if r.ok:
        subdomains.update(re.findall('(?:http.*://)?(?:www.)?([^.]*\.' + domain + ')', r.text))

    # Display the results
    if len(subdomains) > 0:
        print(colored('Subdomains found:', 'green'))
        for subdomain in sorted(subdomains):
            print(colored('- ' + subdomain, 'cyan'))
    else:
        print(colored('No subdomains found.', 'red'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find subdomains for a domain.')
    parser.add_argument('domain', help='The domain to search for subdomains.')
    args = parser.parse_args()

    find_subdomains(args.domain)

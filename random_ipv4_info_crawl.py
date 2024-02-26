import requests
import ipaddress
import random
import pythonping
import json
import os
import time 

from ipwhois import IPWhois
from pprint import pprint
import sys

def generate_random_ipv4():
    # Generate a random IPv4 address
    random_ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
    return random_ip
   

def main():
    while(True): 
        random_ipv4 = generate_random_ipv4()
        print(f"Random IPv4 Address: {random_ipv4}")

        try:
            response = pythonping.ping(random_ipv4, count=4)  # Count is the number of ping packets to send
            if response.rtt_avg is not None:

                print(f"Ping to {random_ipv4} successful. Average Round-Trip Time: {response.rtt_avg} ms")

                try:
                    ipwhois = IPWhois(random_ipv4)
                    result = ipwhois.lookup_rdap()
                    pprint(result)


                    if 'asn' in result:
                        print(f"ASN: {result['asn']}")

                        # File path to store the JSON data
                        output_file_path = random_ipv4 + ".json"

                        # Save results to a local file
                        with open(output_file_path, 'w') as output_file:
                            json.dump(result, output_file, indent=2)
                        
                        url = "https://www."+{random_ipv4}
                        response = requests.get(url)
                
                        html_content =  response.text

                        if html_content:
                            # Process the HTML content as needed
                            print(html_content)

                    if 'asn_description' in result:
                        print(f"ASN Description: {result['asn_description']}")
                    if 'asn_country_code' in result:
                        print(f"Country Code: {result['asn_country_code']}")
                    if 'network' in result:
                        network_info = result['network']
                        if 'name' in network_info:
                            print(f"ISP: {network_info['name']}")
                        if 'registration_date' in network_info:
                            print(f"Registry: {network_info['registration_date']}")
                        if 'handle' in network_info:
                            print(f"Handle: {network_info['handle']}")
                    

                except Exception as e:
                    print(f"Error: {e}")

               

            else:
                print(f"Ping to {ip_address} failed. Check the IP address or network connectivity.")
        except Exception as e:
            print(f"Error: {e}")
    time.sleep(300) 
   

if __name__ == "__main__":
    main()

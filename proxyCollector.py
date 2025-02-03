import requests
import time
import pandas as pd
import random
from concurrent.futures import ThreadPoolExecutor
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("proxy_log.log"), logging.StreamHandler()]
)

# List of reliable endpoints to test proxies
TEST_URLS = [
    "http://httpbin.org/ip",  # Returns your public IP
    "https://api.ipify.org?format=json",  # Returns your public IP in JSON format
    "https://ipinfo.io/json"  # Returns detailed IP information
]

def fetch_proxies_from_proxyscrape(protocol, country_code):
    """
    Fetches proxies from ProxyScrape API.
    :param protocol: The proxy protocol (http, https, socks4, socks5).
    :param country_code: The country code for filtering proxies.
    :return: A list of proxies in "IP:Port" format.
    """
    url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={protocol}&timeout=10000&country={country_code}"
    response = requests.get(url)
    
    if response.status_code == 200:
        proxies = response.text.split("\r\n")  # Split the proxies by newline
        return [proxy for proxy in proxies if proxy.strip()]  # Remove empty strings
    else:
        logging.error(f"Failed to fetch proxies from ProxyScrape for {protocol}: {response.status_code}")
        return []

def fetch_proxies_from_pubproxy(protocol):
    """
    Fetches proxies from PubProxy API.
    :param protocol: The proxy protocol (http, https, socks4, socks5).
    :return: A list of proxies in "IP:Port" format.
    """
    url = f"http://pubproxy.com/api/proxy?format=txt&type={protocol}"
    response = requests.get(url)
    
    if response.status_code == 200:
        proxies = response.text.split("\n")
        return [proxy.strip() for proxy in proxies if proxy.strip()]
    else:
        logging.error(f"Failed to fetch proxies from PubProxy for {protocol}: {response.status_code}")
        return []

def fetch_proxies_from_free_proxy_list():
    """
    Fetches proxies from Free Proxy List website.
    :return: A list of proxies in "IP:Port" format.
    """
    url = "https://www.free-proxy-list.net/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "table-striped"})
            proxies = []
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) > 1:
                    ip = cols[0].text.strip()
                    port = cols[1].text.strip()
                    proxies.append(f"{ip}:{port}")
            return proxies
        else:
            logging.error(f"Failed to fetch proxies from Free Proxy List: {response.status_code}")
            return []
    except Exception as e:
        logging.error(f"Error fetching proxies from Free Proxy List: {e}")
        return []

def fetch_proxies(country_code):
    """
    Fetches proxies from multiple sources for all protocols (http, https, socks4, socks5).
    :param country_code: The country code for filtering proxies.
    :return: A dictionary where keys are protocols and values are lists of proxies.
    """
    protocols = ["http", "https", "socks4", "socks5"]
    all_proxies = {}
    for protocol in protocols:
        proxies = []
        # Fetch proxies from ProxyScrape
        proxies.extend(fetch_proxies_from_proxyscrape(protocol, country_code))
        # Fetch proxies from PubProxy
        proxies.extend(fetch_proxies_from_pubproxy(protocol))
        # Fetch proxies from Free Proxy List (only supports HTTP/HTTPS)
        if protocol in ["http", "https"]:
            proxies.extend(fetch_proxies_from_free_proxy_list())
        # Remove duplicates
        all_proxies[protocol] = list(set(proxies))
    return all_proxies

def measure_latency(proxy, protocol="http"):
    """
    Measures the latency of a proxy by making a request and timing it.
    :param proxy: The proxy in "IP:Port" format.
    :param protocol: The proxy protocol (http, https, socks4, socks5).
    :return: Latency in seconds, or None if the proxy fails.
    """
    proxy_dict = {
        "http": f"{protocol}://{proxy}",
        "https": f"{protocol}://{proxy}"
    }
    try:
        start_time = time.time()
        response = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=10)
        if response.status_code == 200:
            latency = time.time() - start_time
            logging.info(f"Proxy {proxy} ({protocol}) has a latency of {latency:.2f} seconds.")
            return latency
    except Exception as e:
        logging.warning(f"Proxy {proxy} ({protocol}) failed latency test. Error: {e}")
    return None

def test_proxy(proxy, protocol="http", retries=3):
    """
    Tests whether a proxy works by making HTTP requests through it.
    :param proxy: The proxy in "IP:Port" format.
    :param protocol: The proxy protocol (http, https, socks4, socks5).
    :param retries: Number of retry attempts for testing the proxy.
    :return: True if the proxy works, False otherwise.
    """
    proxy_dict = {
        "http": f"{protocol}://{proxy}",
        "https": f"{protocol}://{proxy}"
    }
    for attempt in range(retries):
        for test_url in TEST_URLS:
            try:
                response = requests.get(test_url, proxies=proxy_dict, timeout=10)
                if response.status_code == 200:
                    logging.info(f"Proxy {proxy} ({protocol}) works with {test_url}!")
                    return True
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}: Proxy {proxy} ({protocol}) failed with {test_url}. Error: {e}")
    logging.error(f"Proxy {proxy} ({protocol}) failed all tests.")
    return False

def get_proxy_country(proxy):
    """
    Fetches the country of the given proxy using ip-api.com.
    :param proxy: The proxy in "IP:Port" format.
    :return: The country name if successful, otherwise "Unknown".
    """
    ip = proxy.split(":")[0]  # Extract the IP address from the proxy
    url = f"http://ip-api.com/json/{ip}"  # IP geolocation API endpoint
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data.get("country", "Unknown")
            else:
                logging.error(f"Failed to fetch country for {proxy}: {data.get('message', 'Unknown error')}")
        else:
            logging.error(f"Failed to fetch country for {proxy}: HTTP {response.status_code}")
    except Exception as e:
        logging.error(f"Error fetching country for {proxy}: {e}")
    
    return "Unknown"

def save_working_proxies_to_cache(proxies, filename="proxies_cache.json"):
    """
    Saves working proxies to a JSON file.
    :param proxies: List of working proxies (with protocol and country).
    :param filename: Name of the cache file.
    """
    with open(filename, "w") as f:
        json.dump(proxies, f, indent=4)
    logging.info(f"Saved {len(proxies)} proxies to cache.")

def load_working_proxies_from_cache(filename="proxies_cache.json"):
    """
    Loads working proxies from a JSON file.
    :param filename: Name of the cache file.
    :return: List of cached proxies.
    """
    try:
        with open(filename, "r") as f:
            proxies = json.load(f)
            logging.info(f"Loaded {len(proxies)} proxies from cache.")
            return proxies
    except FileNotFoundError:
        logging.info("No proxy cache found.")
        return []

def add_to_blacklist(proxy, filename="blacklist.txt"):
    """
    Adds a proxy to the blacklist file.
    :param proxy: The proxy in "IP:Port" format.
    :param filename: Name of the blacklist file.
    """
    with open(filename, "a") as f:
        f.write(f"{proxy}\n")
    logging.info(f"Added {proxy} to blacklist.")

def is_blacklisted(proxy, filename="blacklist.txt"):
    """
    Checks if a proxy is blacklisted.
    :param proxy: The proxy in "IP:Port" format.
    :param filename: Name of the blacklist file.
    :return: True if blacklisted, False otherwise.
    """
    try:
        with open(filename, "r") as f:
            blacklist = f.read().splitlines()
        return proxy in blacklist
    except FileNotFoundError:
        return False

def test_proxies_concurrently(proxies, protocol):
    """
    Tests proxies concurrently using multithreading.
    :param proxies: List of proxies to test.
    :param protocol: The proxy protocol (http, https, socks4, socks5).
    :return: List of working proxies.
    """
    working_proxies = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda proxy: (proxy, test_proxy(proxy, protocol)), proxies)
        for proxy, is_working in results:
            if is_working:
                working_proxies.append(proxy)

    return working_proxies

def fetch_and_validate_proxies(country_code, target_country):
    """
    Fetches proxies for all protocols, validates them, and filters them by the specified country.
    :param country_code: The country code for filtering proxies.
    :param target_country: The desired country name (e.g., "United States").
    :return: A list of dictionaries containing working proxies, their protocols, and countries.
    """
    all_proxies = fetch_proxies(country_code)
    working_proxies = []

    for protocol, proxies in all_proxies.items():
        logging.info(f"Fetched {len(proxies)} proxies for {protocol.upper()}...")
        
        # Filter out blacklisted proxies
        proxies = [proxy for proxy in proxies if not is_blacklisted(proxy)]
        
        # Test proxies concurrently
        valid_proxies = test_proxies_concurrently(proxies, protocol)
        
        for proxy in valid_proxies:
            latency = measure_latency(proxy, protocol)
            if latency is not None:
                country = get_proxy_country(proxy)
                logging.info(f"Proxy {proxy} ({protocol}) works and is from {country}. Latency: {latency:.2f}s")
                if country == target_country:  # Filter proxies by country
                    working_proxies.append({"Proxy": proxy, "Protocol": protocol, "Country": country, "Latency": latency})
                time.sleep(1)  # Respect rate limits of the geolocation API
            else:
                add_to_blacklist(proxy)
    
    logging.info(f"Found {len(working_proxies)} working proxies from {target_country}.")
    return working_proxies

# Example usage
if __name__ == "__main__":
    # User inputs
    country_code = input("Enter the country code (e.g., US for USA, GB for UK): ").strip().upper()
    target_country = input("Enter the full country name (e.g., United States, United Kingdom): ").strip()

    # Load cached proxies if available
    cached_proxies = load_working_proxies_from_cache()

    if cached_proxies:
        logging.info("Using cached proxies.")
        working_proxies = cached_proxies
    else:
        # Fetch and validate proxies for all protocols and the specified country
        working_proxies = fetch_and_validate_proxies(country_code, target_country)
        save_working_proxies_to_cache(working_proxies)

    # Save results to an Excel file
    if working_proxies:
        df = pd.DataFrame(working_proxies)
        filename = f"working_proxies_{country_code}.xlsx"
        df.to_excel(filename, index=False)
        logging.info(f"Saved {len(working_proxies)} working proxies to {filename}.")
    else:
        logging.info("No working proxies found.")

# Proxy Scraper & Validator

This script fetches, validates, and filters proxies from multiple free proxy sources. It tests each proxy's latency and availability, then saves working proxies into an Excel file while maintaining a blacklist.

## Features
- Fetches proxies from multiple sources (ProxyScrape, PubProxy, Free Proxy List).
- Supports HTTP, HTTPS, SOCKS4, and SOCKS5 proxies.
- Tests proxies for validity and latency.
- Maintains a blacklist of non-working proxies.
- Saves working proxies to an Excel file.
- Uses multithreading for faster validation.

---

## Installation

### 1. **Clone the Repository**
```sh
git clone [https://github.com/your-repository/proxy-scraper.git](https://github.com/rKrishan99/Proxy-collector-using-Python.git)
cd proxy-scraper
```

### 2. **Install Dependencies**
This script requires Python 3 and the following dependencies:

```sh
pip install requests pandas openpyxl beautifulsoup4
```

---

## Usage

### 1. **Run the Script**
```sh
python script.py
```

### 2. **Enter Required Inputs**
The script will prompt you to enter:
- **Country Code** (e.g., `US` for the USA, `GB` for the UK).

### 3. **Script Process**
1. Clears old proxy files and blacklist.
2. Fetches proxies from different sources.
3. Validates proxies by making test requests.
4. Measures latency for working proxies.
5. Saves working proxies to `working_proxies_<country_code>.xlsx`.

---

## Output Files

- `working_proxies_<country_code>.xlsx` – Contains all working proxies.
- `blacklist.txt` – Stores failed proxies to prevent reuse.
- `proxy_log.log` – Logs script activity.

---

## Troubleshooting

### **1. Proxy List Not Updating?**
Try deleting `blacklist.txt` and rerunning the script.
```sh
rm blacklist.txt
python script.py
```

### **2. Getting Connection Errors?**
- Ensure your internet connection is stable.
- Some proxies may be temporarily unavailable.
- Retry running the script after a few minutes.

---

## License
This project is licensed under the MIT License.

---

## Contributing
Feel free to fork and submit pull requests!

---

## Contact
For any issues, contact rkrishan894@gmail.com.


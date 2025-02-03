# Proxy Fetcher and Validator

A Python-based tool to fetch, validate, and filter proxies from multiple sources (e.g., ProxyScrape, PubProxy, Free Proxy List). The script supports all major protocols (http, https, socks4, socks5), measures proxy latency, filters by country, and saves working proxies to an Excel file.

## Features
- **Fetch Proxies**: Collects proxies from multiple free sources.
- **Validate Proxies**: Tests proxies for functionality using multiple endpoints.
- **Filter by Country**: Filters proxies based on the specified country.
- **Latency Measurement**: Measures the response time of each working proxy.
- **Caching**: Saves validated proxies to a cache file for reuse.
- **Blacklisting**: Avoids retesting non-working proxies by maintaining a blacklist.
- **Multithreading**: Speeds up proxy validation using concurrent testing.
- **Excel Output**: Exports working proxies to an Excel file for easy access.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Input Parameters](#input-parameters)
- [Output Files](#output-files)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)
- [Acknowledgments](#acknowledgments)
- [Disclaimer](#disclaimer)

## Installation

### Prerequisites
- Python 3.6 or higher.
- Access to the internet (to fetch proxies and validate them).

### Steps to Install
#### Clone the Repository:
```bash
git clone [https://github.com/yourusername/proxy-fetcher-validator.git](https://github.com/rKrishan99/Proxy-collector-using-Python.git)
cd proxy-fetcher-validator
```

#### Install Dependencies:
Install the required Python libraries using pip:
```bash
pip install -r requirements.txt
```
The `requirements.txt` file includes:
- `requests`: For making HTTP requests.
- `pandas`: For saving results to Excel.
- `beautifulsoup4`: For scraping proxies from websites.
- `openpyxl`: For Excel file support.

#### Verify Installation:
Run the following command to ensure everything is installed correctly:
```bash
python --version
pip list
```

## Usage

### Run the Script
To run the script, execute the following command:
```bash
python find_proxies.py
```
The script will prompt you for two inputs:
1. **Country Code**: The ISO 3166-1 alpha-2 country code (e.g., GB for the UK, US for the USA).
2. **Target Country Name**: The full name of the country (e.g., "United Kingdom", "United States").

#### Example:
```bash
Enter the country code (e.g., US for USA, GB for UK): GB
Enter the full country name (e.g., United States, United Kingdom): United Kingdom
```

## Input Parameters

1. **Country Code**
   - Format: ISO 3166-1 alpha-2 (e.g., GB for the UK, US for the USA).
   - Purpose: Filters proxies by the specified country.
2. **Target Country Name**
   - Format: Full country name (e.g., "United Kingdom", "United States").
   - Purpose: Ensures only proxies from the desired country are saved.

## Output Files

1. **Excel File**
   - Filename: `working_proxies_<country_code>.xlsx` (e.g., `working_proxies_GB.xlsx`).
   - Columns:
     - `Proxy`: The proxy in IP:Port format.
     - `Protocol`: The protocol supported by the proxy (http, https, socks4, socks5).
     - `Country`: The country of origin for the proxy.
     - `Latency (s)`: The response time of the proxy in seconds.

2. **Cache File**
   - Filename: `proxies_cache.json`.
   - Purpose: Stores validated proxies for future reuse, avoiding redundant testing.

3. **Blacklist File**
   - Filename: `blacklist.txt`.
   - Purpose: Maintains a list of non-working proxies to avoid retesting them.

## Dependencies

The script relies on the following Python libraries:
- `requests`: For making HTTP requests.
- `pandas`: For saving results to Excel.
- `beautifulsoup4`: For scraping proxies from websites.
- `openpyxl`: For Excel file support.

You can install these dependencies using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

## Contributing

We welcome contributions to improve this project! Here’s how you can contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add your commit message here"
   ```
4. Push your changes to GitHub:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a pull request with a detailed description of your changes.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue in the **GitHub Issues** section. Alternatively, you can contact me directly via email: rkrishan894@gmail.com`.

## Acknowledgments

### Proxy Sources:
- ProxyScrape
- PubProxy
- Free Proxy List

### Geolocation API:
- [ip-api.com](http://ip-api.com)

## Disclaimer

This tool is intended for **educational and ethical purposes only**. Please ensure that you comply with the terms of service of the websites you interact with when using proxies. **Misuse of proxies may violate laws or terms of service.**

---
**Happy Proxy Hunting! 🚀**


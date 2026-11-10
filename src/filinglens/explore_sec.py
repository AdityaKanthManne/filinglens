###Import the requests library.

import requests
import os
import sys
#Store Apple's CIK as a ten-character string.

CIK_app="0000320193"

#Construct the SEC submissions endpoint using the CIK.

url=f"https://data.sec.gov/submissions/CIK{CIK_app}.json"

#Create an HTTP GET request that includes a descriptive User-Agent header with your real contact email.
user_agent= os.getenv("SEC_USER_AGENT")
if not user_agent:
    raise ValueError("SEC_USER_AGENT environment variable not set")
headers={"User-Agent": user_agent}

#Check whether the HTTP response succeeded.





try:
    response = requests.get(url,headers=headers, timeout=15)
    response.raise_for_status()

except requests.exceptions.HTTPError as e:
    print(f"HTTP Error: {e}")
    sys.exit(1)
except requests.exceptions.ConnectionError as e:
    print(f"Connection Error: {e}")
    sys.exit(1)
except requests.exceptions.Timeout as e:
    print(f"Timeout Error: {e}")
    sys.exit(1)






#Convert the JSON response into Python data.

data = response.json()
print(data.keys())
#Print the company's name, CIK, and ticker symbols.


print(f"Company Name: {data.get('name')}")
print(f"CIK: {data.get('cik')}")
print(f"Ticker: {data.get('tickers')}")


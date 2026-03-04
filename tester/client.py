import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class APIClient:
    def __init__(self, base_url, timeout=3, max_retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            response = self.session.request(
                method, 
                url, 
                timeout=self.timeout, 
                **kwargs
            )
            latency = (time.time() - start_time) * 1000
            return response, latency, None
        except requests.exceptions.RequestException as e:
            latency = (time.time() - start_time) * 1000
            return None, latency, str(e)

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

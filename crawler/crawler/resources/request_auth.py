import requests
from requests.auth import AuthBase
from crawler.settings import settings

if __name__ == "__main__":
    url = "http://ec2-13-250-100-229.ap-southeast-1.compute.amazonaws.com:8000/api/test_admin_only"
    resp = requests.get(url, headers={"Authorization": f"Bearer {settings.ACCESS_TOKEN}"})
    print(resp.json())

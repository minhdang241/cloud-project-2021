import requests
from requests.auth import AuthBase
import datetime
import json
if __name__ == "__main__":
    url = "http://ec2-13-250-100-229.ap-southeast-1.compute.amazonaws.com:8000/api/requests"
    payload = json.dumps({
      "request_id": "17",
      "updated_at": str(datetime.datetime.utcnow()),
      "request_metadata": {"total_item": 13},
      "status": "FINISHED"
    })
    resp = requests.put("http://ec2-13-250-100-229.ap-southeast-1.compute.amazonaws.com:8000/api/requests", data=payload, headers={"Content-Type": "application/json; charset=utf-8"})
    print(resp.json())

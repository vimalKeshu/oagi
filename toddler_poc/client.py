import requests
import base64
import json

oagi_url='http://127.0.0.1:5000/retry'
url = 'https://www.poorvimal.com'
timeout_seconds = 1  # Set your desired timeout value in seconds
recoverable=True 

while(recoverable):
    try:
        response = requests.get(url, timeout=timeout_seconds)
        if response.status_code == 200:
            print(response.text)
        else:
            print(f'Error: {response.status_code}')
    except requests.RequestException as e:
        # Handle other request exceptions
        #print(f'Request error: {e}')
        error_message = str(e)
        data = {'error': base64.b64encode(error_message.encode()).decode('utf-8')}
        print(data)
        try:
           res = requests.post(oagi_url, json=data, headers={"Content-Type": "application/json"},)
           t = json.loads(res.text)
           print(t) 
           if t['retry'] > 0.5:
               recoverable=True
           else:
               recoverable=False
        except Exception as e:
            print(e)
            recoverable=False
        
        

import os 
import time 

import pathlib
import textwrap

import google.generativeai as genai

prompt = """What is the probability of retrying below operation resolve the issue ? please answer in json.
Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation:
{"retry": probability in float}
Error:
Caused by: org.apache.iceberg.shaded.org.apache.hc.client5.http.HttpHostConnectException: Connect to http://127.0.0.1:8181 [/127.0.0.1] failed: Connection refused (Connection refused)
	at java.base/java.net.PlainSocketImpl.socketConnect(Native Method)
	at java.base/java.net.AbstractPlainSocketImpl.doConnect(AbstractPlainSocketImpl.java:412)
	at java.base/java.net.AbstractPlainSocketImpl.connectToAddress(AbstractPlainSocketImpl.java:255)
	at java.base/java.net.AbstractPlainSocketImpl.connect(AbstractPlainSocketImpl.java:237)
	at java.base/java.net.SocksSocketImpl.connect(SocksSocketImpl.java:392)
	at java.base/java.net.Socket.connect(Socket.java:609)
"""

GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt,
                                  generation_config=genai.types.GenerationConfig(temperature=0.0)
                                  )

try:
  print(response.text)
except Exception as e:
  print(f'{type(e).__name__}: {e}')




# FastAPI id_token valdation
This code demonstrates how to correctly validate a user token (id_token) in auth0.

Here is how to use it:
1. Start theserver by running `python app.py`
2. in another python session run th following:
```python
import requests

id_token = "YOUR_ID_TOKEN_HERE"

response = requests.get(
    'http://localhost:8000/user',
    headers={'Authorization': f'Bearer {id_token}'}
)

print(response.json())
```

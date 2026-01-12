import requests
purchase_url = "https://ozymandias.ctf.clawtheflag.com/purchase"
purchase_data = {
    "flag_id": "heisenberg",
    "location": "Albuquerque"
}

r = requests.post(purchase_url, json=purchase_data, cookies=cookies, headers=headers)
print(r.json())

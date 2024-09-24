import requests
from anticaptchaofficial.recaptchav3proxyless import recaptchaV3Proxyless

# First HttpRequest Block (initial request)
url = "https://idpsesion.app.flow.com.ar/openam/json/realms/root/realms/convergente/authenticate?authIndexType=service&authIndexValue=sdkRecaptchaAuthentication"
headers = {
    "Host": "idpsesion.app.flow.com.ar",
    "Connection": "keep-alive",
    "Content-Length": "0",
    "accept-api-version": "protocol=1.0,resource=2.1",
    "sec-ch-ua": "\"Google Chrome\";v=\"123\", \"Not:A-Brand\";v=\"8\", \"Chromium\";v=\"123\"",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "content-type": "application/json",
    "accept": "application/json",
    "app-id": "oidc-web-flow",
    "x-requested-with": "forgerock-sdk",
    "sec-ch-ua-platform": "\"Windows\"",
    "Origin": "https://web.app.flow.com.ar",
    "Sec-Fetch-Site": "same-site",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://web.app.flow.com.ar/",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
}

response = requests.post(url, headers=headers)
data = response.json()

# Parse Block (extracting authId)
auth_id = data.get('authId')

# SolveRecaptchaV3 Block using AntiCaptcha
api_key = "YOUR_ANTI_CAPTCHA_API_KEY"  # replace with your AntiCaptcha API key
site_key = "6LdVlxEnAAAAAM03LzCP3rX3GITJa6JDLc6w5gPb"
site_url = "https://web.app.flow.com.ar/login"

solver = recaptchaV3Proxyless()
solver.set_verbose(1)
solver.set_key(api_key)
solver.set_website_url(site_url)
solver.set_website_key(site_key)
solver.set_min_score(0.9)

recaptcha_token = solver.solve_and_return_solution()

if recaptcha_token != 0:
    print(f"Recaptcha solved: {recaptcha_token}")
else:
    print(f"Error solving recaptcha: {solver.error_code}")
    recaptcha_token = None  # handle error case

# Check if recaptcha_token was solved
if recaptcha_token:
    # Length Block (preparing the final payload)
    payload = {
        "authId": auth_id,
        "callbacks": [
            {
                "type": "NameCallback",
                "output": [{"name": "prompt", "value": "User Name"}],
                "input": [{"name": "IDToken1", "value": "<input.USER>"}],  # Replace with user input
                "_id": 0
            },
            {
                "type": "PasswordCallback",
                "output": [{"name": "prompt", "value": "Password"}],
                "input": [{"name": "IDToken2", "value": "<input.PASS>"}],  # Replace with password
                "_id": 1
            },
            {
                "type": "HiddenValueCallback",
                "output": [{"name": "value", "value": ""}, {"name": "id", "value": "recaptcha_token"}],
                "input": [{"name": "IDToken3", "value": recaptcha_token}],
                "_id": 2
            }
        ],
        "status": 200,
        "ok": True
    }

    # Final HttpRequest Block
    final_url = url
    final_headers = {
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es-ES,es;q=0.9",
        "Connection": "keep-alive",
        "Host": "idpsesion.app.flow.com.ar",
        "Origin": "https://web.app.flow.com.ar",
        "Referer": "https://web.app.flow.com.ar/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        "accept": "application/json",
        "accept-api-version": "protocol=1.0,resource=2.1",
        "app-id": "oidc-web-flow",
        "content-type": "application/json",
        "sec-ch-ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Google Chrome\";v=\"128\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "x-requested-with": "forgerock-sdk"
    }

    final_response = requests.post(final_url, json=payload, headers=final_headers)
    print(final_response.json())
else:
    print("Recaptcha token could not be obtained.")
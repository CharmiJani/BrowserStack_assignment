## API Integration

The project uses the **RapidAPI Deep Translate API** to translate Spanish article titles into English.

The API call is implemented in the `translate_text()` function in `main.py` using the `requests` library.

Example API request:

response = requests.post(url, json=payload, headers=headers)

The API key is stored securely in a `.env` file and loaded using `python-dotenv` to avoid exposing credentials in the source code.

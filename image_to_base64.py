import base64
import json
import urllib.request

def handle(params):
    if isinstance(params, str):
        params = json.loads(params)

    image_url = params.get("image_url")

    if not image_url:
        return {
            "success": False,
            "error": "image_url is required"
        }

    try:
        with urllib.request.urlopen(image_url, timeout=20) as response:
            image_data = response.read()

        image_base64 = base64.b64encode(image_data).decode("utf-8")

        return {
            "success": True,
            "image_base64": image_base64
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

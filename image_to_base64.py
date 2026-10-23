import base64
import requests

def handle(params):
    image_url = params.get("image_url")

    if not image_url:
        return {
            "success": False,
            "error": "image_url is required"
        }

    try:
        response = requests.get(image_url, timeout=20)
        response.raise_for_status()

        image_base64 = base64.b64encode(response.content).decode("utf-8")

        return {
            "success": True,
            "image_base64": image_base64
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

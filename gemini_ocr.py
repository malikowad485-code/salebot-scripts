import json
import urllib.request
import urllib.error

def handle(params):
    if isinstance(params, str):
        params = json.loads(params)

    image_base64 = params.get("image_base64")
    gemini_key = params.get("gemini_key")
    model = params.get("model", "gemini-2.0-flash")

    if not image_base64:
        return {
            "success": False,
            "error": "image_base64 is required"
        }

    if not gemini_key:
        return {
            "success": False,
            "error": "gemini_key is required"
        }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + model
        + ":generateContent"
    )

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Прочитай весь текст на фотографии. Верни только распознанный текст, без комментариев."
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }
        ]
    }

    data = json.dumps(body).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": gemini_key
        }
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))

        text = (
            result
            .get("candidates", [{}])[0]
            .get("content", {})
            .get("parts", [{}])[0]
            .get("text", "")
        )

        return {
            "success": True,
            "ocr_text": text
        }

    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")

        return {
            "success": False,
            "error": f"HTTP {e.code}: {error_body}"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

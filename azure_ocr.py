import json
import time
import urllib.request

def handle(params):
    if isinstance(params, str):
        params = json.loads(params)

    image_url = params.get("image_url")
    api_key = params.get("azure_key")
    endpoint = params.get("azure_endpoint", "https://darya.cognitiveservices.azure.com")

    if not image_url:
        return {"success": False, "error": "image_url is required"}

    if not api_key:
        return {"success": False, "error": "azure_key is required"}

    analyze_url = endpoint.rstrip("/") + "/vision/v3.2/read/analyze"

    try:
        # 1. Отправляем фото в Azure
        body = json.dumps({"url": image_url}).encode("utf-8")

        request = urllib.request.Request(
            analyze_url,
            data=body,
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Ocp-Apim-Subscription-Key": api_key
            }
        )

        with urllib.request.urlopen(request, timeout=30) as response:
            operation_url = response.headers.get("Operation-Location")

        if not operation_url:
            return {
                "success": False,
                "error": "Operation-Location header not found"
            }

        # 2. Ждём обработку
        time.sleep(5)

        # 3. Получаем результат
        result_request = urllib.request.Request(
            operation_url,
            method="GET",
            headers={
                "Ocp-Apim-Subscription-Key": api_key
            }
        )

        with urllib.request.urlopen(result_request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        # 4. Собираем весь текст
        lines = []

        read_results = result.get("analyzeResult", {}).get("readResults", [])

        for page in read_results:
            for line in page.get("lines", []):
                lines.append(line.get("text", ""))

        ocr_text = "\n".join(lines)

        return {
            "success": True,
            "status": result.get("status"),
            "ocr_text": ocr_text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

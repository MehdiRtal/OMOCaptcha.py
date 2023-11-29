import httpx
import time
import base64


class OMOCaptcha:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def create_job(self, service_id: int, **data):
        r = httpx.post("https://omocaptcha.com/api/createJob", json={
            "api_token": self.api_key,
            "data": {
                "type_job_id": service_id,
                **data
            }
        })
        if r.json()["error"]:
            raise Exception(r.json()["message"])
        return r.json()["job_id"]

    def get_result(self, job_id: int):
        while True:
            r = httpx.post("https://omocaptcha.com/api/getJobResult", json={
            "api_token": self.api_key,
            "job_id": job_id
            })
            if r.json()["status"] == "waiting":
                time.sleep(3)
            elif r.json()["status"] == "fail":
                raise Exception()
            elif r.json()["status"] == "success":
                return r.json()["result"]

    def solve_tiktok_2objects(self, image_url: str):
        image_content = httpx.get(image_url).content
        job_id = self.create_job(22, image_base64=base64.b64encode(image_content).decode("utf-8"), width_view=340, height_view=212)
        result = self.get_result(job_id)
        return float(result.split("|")[0]), float(result.split("|")[1]), float(result.split("|")[2]), float(result.split("|")[3])

    def solve_tiktok_rotation(self, outer_image_url: str, inner_image_url: str):
        outer_image_content = httpx.get(outer_image_url).content
        inner_image_content = httpx.get(inner_image_url).content
        job_id = self.create_job(23, image_base64=f"{base64.b64encode(inner_image_content).decode('utf-8')}|{base64.b64encode(outer_image_content).decode('utf-8')}")
        result = self.get_result(job_id)
        return int(result)

    def solve_tiktok_drag_drop(self, image_url: str):
        image_content = httpx.get(image_url).content
        job_id = self.create_job(24, image_base64=base64.b64encode(image_content).decode("utf-8"), width_view=340)
        result = self.get_result(job_id)
        return int(result)

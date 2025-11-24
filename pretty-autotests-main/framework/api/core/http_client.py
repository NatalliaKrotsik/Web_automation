import os
from dotenv import load_dotenv
import requests
import json
import allure
from typing import Any, Dict, Optional

from framework.logger import logger

load_dotenv()

class HttpClient:
    """
    Base HTTP client that centralizes URL building, logging, and Allure attachments.
    Provides convenience methods for GET, POST, PUT, PATCH, DELETE.
    """

    def __init__(self, default_headers: Optional[Dict[str, str]] = None):
        # Normalize base URL
        self.base_url = os.getenv("API_URL_DEV")
        # Initialize a session
        self.session = requests.Session()
        if default_headers:
            self.update_headers(default_headers)

    def _build_url(self, path: str) -> str:
        """
        Combine base_url and endpoint path into a full URL.
        """
        return f"{self.base_url}/{path.lstrip('/')}"

    def _attach_allure(self, response: requests.Response) -> None:
        """
        Attach request and response details (including redirects) to Allure report.
        """
        indent = 4

        def dump_body(resp: requests.Response) -> str:
            try:
                return json.dumps(resp.json(), indent=indent)
            except Exception:
                return resp.text or ""

        # Attach outgoing request
        req = response.request
        with allure.step(f"Request: {req.method} {req.url}"):
            allure.attach(
                name="Headers",
                body=json.dumps(dict(req.headers), indent=indent),
                attachment_type=allure.attachment_type.JSON,
            )
            if req.body:
                try:
                    pretty = json.dumps(json.loads(req.body), indent=indent)
                except Exception:
                    pretty = (
                        req.body.decode()
                        if isinstance(req.body, bytes)
                        else str(req.body)
                    )
                allure.attach(
                    name="Body",
                    body=pretty,
                    attachment_type=allure.attachment_type.JSON,
                )

        # Attach history responses + final response
        for resp in response.history + [response]:
            with allure.step(f"Response: {resp.status_code} {resp.reason}"):
                allure.attach(
                    name="Headers",
                    body=json.dumps(dict(resp.headers), indent=indent),
                    attachment_type=allure.attachment_type.JSON,
                )
                allure.attach(
                    name="Body",
                    body=dump_body(resp),
                    attachment_type=allure.attachment_type.JSON,
                )

    @allure.step("{method} {path}")
    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Any] = None,
        **kwargs: Any,
    ) -> requests.Response:
        """
        Core request method that performs the HTTP call, logging, and Allure attachments.
        """
        url = self._build_url(path)
        logger.debug(
            f"[HTTP] {method} {url} | params={params} json={json_body} kwargs={kwargs}"
        )
        resp = self.session.request(
            method=method, url=url, params=params, json=json_body, **kwargs
        )
        self._attach_allure(resp)
        return resp

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def update_headers(
        self, default_headers: Optional[Dict[str, str]]
    ) -> None:
        self.session.headers.update(default_headers)

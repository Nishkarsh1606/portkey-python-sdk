"""Rubeus implementation."""
import os
from typing import Optional, Union, Mapping, Any
from .global_constants import (
    MISSING_API_KEY_ERROR_MESSAGE,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
)
from .base_client import APIClient
from . import apis

__all__ = ["Rubeus"]


class Rubeus(APIClient):
    completion: apis.Completions
    chat_completion: apis.ChatCompletions

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: Union[float, None] = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Optional[Mapping[str, str]] = None,
        default_query: Optional[Mapping[str, object]] = None,
        default_params: Optional[Mapping[str, Any]] = None,
    ) -> None:
        if base_url is None:
            self.base_url = "https://api.portkey.ai"
        self.api_key = api_key or os.environ.get("PORTKEY_API_KEY") or ""
        if not self.api_key:
            raise ValueError(MISSING_API_KEY_ERROR_MESSAGE)
        self.default_params = default_params or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers
        self.default_query = default_query
        super().__init__(
            base_url=self.base_url,
            api_key=self.api_key,
            timeout=self.timeout,
            max_retries=self.max_retries,
            custom_headers=self.default_headers,
            custom_query=self.default_query,
            custom_params=self.default_params,
        )
        self.completion = apis.Completions(self)
        self.chat_completion = apis.ChatCompletions(self)

    def __setitem__(self, key: str, value: Any) -> None:
        setattr(self, key, value)
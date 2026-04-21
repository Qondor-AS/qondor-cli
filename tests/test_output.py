"""Tests for output formatting."""

from __future__ import annotations

import json

from qondor_api_sdk import ApiModel

from qondor_cli._output import format_output


class _FakeModel(ApiModel):
    id: int | None = None
    some_name: str | None = None


class TestFormatOutput:
    def test_pretty_json_single_model(self):
        model = _FakeModel(id=1, some_name="hello")
        result = format_output(model, raw=False)
        parsed = json.loads(result)
        assert parsed["id"] == 1
        assert parsed["someName"] == "hello"
        assert "\n" in result  # pretty-printed

    def test_raw_json_single_model(self):
        model = _FakeModel(id=1, some_name="hello")
        result = format_output(model, raw=True)
        parsed = json.loads(result)
        assert parsed["id"] == 1
        assert "\n" not in result  # compact

    def test_pretty_json_list(self):
        models = [_FakeModel(id=1, some_name="a"), _FakeModel(id=2, some_name="b")]
        result = format_output(models, raw=False)
        parsed = json.loads(result)
        assert len(parsed) == 2
        assert parsed[0]["id"] == 1

    def test_raw_json_list(self):
        models = [_FakeModel(id=1, some_name="a")]
        result = format_output(models, raw=True)
        assert "\n" not in result

    def test_none_result(self):
        result = format_output(None, raw=False)
        assert result == ""

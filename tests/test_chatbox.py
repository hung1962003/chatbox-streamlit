"""Unit tests for streamlit-chatbox (session helpers + export/import)."""

from __future__ import annotations

import streamlit as st

from streamlit_chatbox import ChatBox, Json, Markdown
from streamlit_chatbox.elements import OutputElement, Video


class _Session(dict):
    """Minimal stand-in for st.session_state."""

    def __getattr__(self, item):
        try:
            return self[item]
        except KeyError as exc:
            raise AttributeError(item) from exc

    def __setattr__(self, key, value):
        self[key] = value


def _bind_session(monkeypatch) -> _Session:
    state = _Session()
    monkeypatch.setattr(st, "session_state", state)
    return state


def test_to_dict_from_dict_roundtrip(monkeypatch):
    _bind_session(monkeypatch)
    box = ChatBox(session_key="cb_test")
    box.use_chat_name("chat1")
    box.history.append(
        {"role": "user", "elements": [Markdown("hello")], "metadata": {}}
    )
    box.history.append(
        {"role": "assistant", "elements": [Markdown("world")], "metadata": {}}
    )
    box.context["temperature"] = 0.2

    payload = box.to_dict()
    restored = ChatBox(session_key="cb_test").from_dict(payload)

    assert restored.cur_chat_name == "chat1"
    assert len(restored.history) == 2
    assert restored.history[0]["role"] == "user"
    assert restored.history[0]["elements"][0].content == "hello"
    assert restored.history[1]["elements"][0].content == "world"
    assert restored.context["temperature"] == 0.2


def test_context_to_session_honors_exclude(monkeypatch):
    state = _bind_session(monkeypatch)
    box = ChatBox(session_key="cb_ctx")
    box.use_chat_name("default")
    box.context["keep"] = 1
    box.context["drop"] = 2

    box.context_to_session(exclude=["drop"])
    assert state["keep"] == 1
    assert "drop" not in state


def test_change_and_delete_chat_name(monkeypatch):
    _bind_session(monkeypatch)
    box = ChatBox(session_key="cb_names")
    box.use_chat_name("a")
    box.history.append(
        {"role": "user", "elements": [Markdown("in a")], "metadata": {}}
    )
    assert box.change_chat_name("b") is True
    assert box.cur_chat_name == "b"
    assert "a" not in box.get_chat_names()

    box.use_chat_name("extra")
    box.del_chat_name("extra")
    assert "extra" not in box.get_chat_names()
    assert box.cur_chat_name in box.get_chat_names()


def test_output_element_json_roundtrip():
    element = Json({"ok": True}, title="payload")
    restored = OutputElement.from_dict(element.to_dict())
    assert isinstance(restored, Json)
    assert '"ok"' in restored.content


def test_video_default_kwargs_applied():
    video = Video("clip.mp4")
    assert video._kwargs.get("format") == "mp4"

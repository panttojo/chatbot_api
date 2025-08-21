from unittest.mock import MagicMock, patch

from openai import APITimeoutError, AuthenticationError, RateLimitError

from core.bots.openai import OpenAIBot
from core.bots.schemas import ChatErrorResponse


@patch("core.bots.openai.OpenAI")
def test_chat_authentication_error(mock_openai: MagicMock) -> None:
    """Test that AuthenticationError is handled correctly."""
    mock_client = MagicMock()
    mock_client.responses.create.side_effect = AuthenticationError(
        message="auth error", response=MagicMock(), body=None
    )
    mock_openai.return_value = mock_client

    bot = OpenAIBot()
    response = bot.chat("hello")

    assert isinstance(response, ChatErrorResponse)
    assert response.output_text == "Ocurrió un error, por favor contacta al administrador."
    mock_client.responses.create.assert_called_once()


@patch("core.bots.openai.OpenAI")
def test_chat_rate_limit_error(mock_openai: MagicMock) -> None:
    """Test that RateLimitError is handled correctly."""
    mock_client = MagicMock()
    mock_client.responses.create.side_effect = RateLimitError(message="rate limit", response=MagicMock(), body=None)
    mock_openai.return_value = mock_client

    bot = OpenAIBot()
    response = bot.chat("hello")

    assert isinstance(response, ChatErrorResponse)
    assert response.output_text == "Ocurrió un error, por favor intenta más tarde."
    mock_client.responses.create.assert_called_once()


@patch("core.bots.openai.OpenAI")
def test_chat_api_timeout_error(mock_openai: MagicMock) -> None:
    """Test that APITimeoutError is handled correctly."""
    mock_client = MagicMock()
    mock_client.responses.create.side_effect = APITimeoutError(request=MagicMock())
    mock_openai.return_value = mock_client

    bot = OpenAIBot()
    response = bot.chat("hello")

    assert isinstance(response, ChatErrorResponse)
    assert response.output_text == "Ocurrió un error, por favor intenta más tarde."
    mock_client.responses.create.assert_called_once()


@patch("core.bots.openai.OpenAI")
def test_chat_generic_exception(mock_openai: MagicMock) -> None:
    """Test that a generic Exception is handled correctly."""
    error_message = "A generic error occurred"
    mock_client = MagicMock()
    mock_client.responses.create.side_effect = Exception(error_message)
    mock_openai.return_value = mock_client

    bot = OpenAIBot()
    response = bot.chat("hello")

    assert isinstance(response, ChatErrorResponse)
    assert response.output_text == error_message
    mock_client.responses.create.assert_called_once()

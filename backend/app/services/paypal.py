"""Thin async client for the PayPal REST API (Orders v2, Payments v2, Payouts v1).

Flow Pactora uses:
    1. create_order(amount)            -> buyer approves via the returned "approve" link
    2. authorize_order(order_id)       -> funds are held (escrow-like)
    3. capture_authorization(auth_id)  -> funds are captured once the deal is delivered
    4. create_payout(email, amount)    -> freelancer gets paid
"""

import time
import uuid
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

import httpx

from app.config import get_settings

_TIMEOUT = httpx.Timeout(30.0)

# Simple in-process token cache. PayPal tokens last ~9 hours.
_token: str | None = None
_token_expires_at: float = 0.0


class PayPalError(Exception):
    def __init__(self, status_code: int, body: Any):
        self.status_code = status_code
        self.body = body
        super().__init__(f"PayPal API error {status_code}: {body}")


def _format_amount(amount: Decimal | float | int | str) -> str:
    return str(Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def _parse(resp: httpx.Response) -> dict[str, Any]:
    if resp.is_error:
        try:
            body: Any = resp.json()
        except ValueError:
            body = resp.text
        raise PayPalError(resp.status_code, body)
    return resp.json() if resp.content else {}


async def get_access_token(force_refresh: bool = False) -> str:
    """Fetch (and cache) an OAuth2 access token via client credentials."""
    global _token, _token_expires_at

    if not force_refresh and _token and time.time() < _token_expires_at:
        return _token

    settings = get_settings()
    if not settings.paypal_client_id or not settings.paypal_client_secret:
        raise RuntimeError("PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET must be set")

    async with httpx.AsyncClient(base_url=settings.paypal_base_url, timeout=_TIMEOUT) as client:
        resp = await client.post(
            "/v1/oauth2/token",
            auth=(settings.paypal_client_id, settings.paypal_client_secret),
            data={"grant_type": "client_credentials"},
            headers={"Accept": "application/json"},
        )
    data = _parse(resp)

    _token = data["access_token"]
    # Refresh a minute early to avoid using a token right as it expires.
    _token_expires_at = time.time() + int(data.get("expires_in", 0)) - 60
    return _token


async def _request(method: str, path: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
    settings = get_settings()
    token = await get_access_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
        # Idempotency key so retried POSTs don't double-charge/double-pay.
        "PayPal-Request-Id": str(uuid.uuid4()),
    }
    async with httpx.AsyncClient(base_url=settings.paypal_base_url, timeout=_TIMEOUT) as client:
        resp = await client.request(method, path, json=json, headers=headers)
    return _parse(resp)


async def create_order(
    amount: Decimal | float | int | str,
    intent: str = "AUTHORIZE",
    currency: str = "USD",
) -> dict[str, Any]:
    """Create an order. The buyer must approve it (links[rel=approve]) before authorizing."""
    payload = {
        "intent": intent,
        "purchase_units": [
            {"amount": {"currency_code": currency, "value": _format_amount(amount)}}
        ],
    }
    return await _request("POST", "/v2/checkout/orders", json=payload)


async def authorize_order(order_id: str) -> dict[str, Any]:
    """Authorize an approved order. The authorization id is at
    purchase_units[0].payments.authorizations[0].id."""
    return await _request("POST", f"/v2/checkout/orders/{order_id}/authorize", json={})


async def capture_authorization(authorization_id: str) -> dict[str, Any]:
    """Capture previously authorized funds."""
    return await _request(
        "POST", f"/v2/payments/authorizations/{authorization_id}/capture", json={}
    )


async def create_payout(
    email: str,
    amount: Decimal | float | int | str,
    currency: str = "USD",
    note: str = "Payment via Pactora",
) -> dict[str, Any]:
    """Send money to a PayPal account by email."""
    batch_id = f"pactora-{uuid.uuid4().hex}"
    payload = {
        "sender_batch_header": {
            "sender_batch_id": batch_id,
            "email_subject": "You've been paid via Pactora",
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "receiver": email,
                "amount": {"value": _format_amount(amount), "currency": currency},
                "note": note,
                "sender_item_id": batch_id,
            }
        ],
    }
    return await _request("POST", "/v1/payments/payouts", json=payload)

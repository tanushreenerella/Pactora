from fastapi import APIRouter, HTTPException

from app.services import paypal

router = APIRouter(prefix="/paypal", tags=["paypal"])


@router.get("/test")
async def paypal_test() -> dict[str, str]:
    """Verify PayPal credentials by fetching a fresh access token."""
    try:
        await paypal.get_access_token(force_refresh=True)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except paypal.PayPalError as exc:
        raise HTTPException(status_code=502, detail=f"PayPal auth failed ({exc.status_code})") from exc
    return {"status": "ok", "token": "ok"}

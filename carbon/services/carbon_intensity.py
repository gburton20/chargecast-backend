from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

import requests

BASE_URL = os.getenv("CARBON_INTENSITY_BASE_URL", "https://api.carbonintensity.org.uk")
TIMEOUT = 10 # seconds

class CarbonIntensityError(Exception):
    pass

def _request(path: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    url = f"{BASE_URL.rstrip('/')}/{path.lstrip('/')}"
    try: 
        resp = requests.get(url, params=params, timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as exc:
        raise CarbonIntensityError(f"Error calling Carbon Intensity API: {exc}") from exc
    
    if "data" not in data:
        raise CarbonIntensityError("Unexpected response format from Carbon Intensity API: {data}")
    
    return data

def _format_neso_datetime(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)

    return dt.strftime("%Y-%m-%dT%H:%MZ")

def get_regional_intensity_range(
    postcode: str,
    from_dt: datetime,
    to_dt: datetime,
) -> List[Dict[str, Any]]:
    # Calls: /regional/intensity/{from}/{to}/postcode/{postcode}
    # Returns the raw 'data' list from NESO.
    from_str = _format_neso_datetime(from_dt)
    to_str = _format_neso_datetime(to_dt)

    path = f"/regional/intensity/{from_str}/{to_str}/postcode/{postcode}"

    data = _request(path)
    return data["data"]

def get_seven_day_history(postcode: str) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=7)
    return get_regional_intensity_range(postcode=postcode, from_dt=start, to_dt=now)

def get_current_30_min_forecast(postcode: str) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    end = now + timedelta(minutes = 30)
    return get_regional_intensity_range(postcode=postcode, from_dt=now, to_dt=end)

def get_48h_forecast(postcode: str) -> List[Dict[str, Any]]:
    now = datetime.now(timezone.utc)
    end = now + timedelta(hours=48)
    return get_regional_intensity_range(postcode=postcode, from_dt=now, to_dt=end)
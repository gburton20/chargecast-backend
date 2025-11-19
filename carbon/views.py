from django.shortcuts import render
from urllib.parse import unquote

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .services.carbon_intensity import (
    get_seven_day_history,
    get_current_30_min_forecast,
    get_48h_forecast,
    CarbonIntensityError,
)

@api_view(["GET"])
def health(request):
    return Response({"status": "ok"}, status=status.HTTP_200_OK)

def _get_postcode_from_request(request):
    postcode = request.query_params.get("postcode")
    if not postcode:
        raise ValueError("Missing required query parameter: 'postcode'")
    # Django REST Framework automatically decodes URL parameters,
    # but ensure any double-encoding is handled
    postcode = unquote(postcode)
    return postcode.strip()

@api_view(["GET"])
def regional_history_7d(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_seven_day_history(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    # Extract region metadata from first data point
    region_info = {}
    if data and isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict):
            region_info = {
                'region': first_item.get('region'),
                'shortname': first_item.get('shortname'),
                'regionid': first_item.get('regionid'),
                'dnoregion': first_item.get('dnoregion')
            }
    
    # Return full postcode and region info for partner's Streamlit components
    return Response({"data": data, "postcode": postcode, **region_info})

@api_view(["GET"])
def regional_current_30m(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_current_30_min_forecast(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    # Extract region metadata from first data point
    region_info = {}
    if data and isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict):
            region_info = {
                'region': first_item.get('region'),
                'shortname': first_item.get('shortname'),
                'regionid': first_item.get('regionid'),
                'dnoregion': first_item.get('dnoregion')
            }
    
    # Return full postcode and region info for partner's Streamlit components
    return Response({"data": data, "postcode": postcode, **region_info})

@api_view(["GET"])
def regional_forecast_48h(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_48h_forecast(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    # Extract region metadata from first data point
    region_info = {}
    if data and isinstance(data, list) and len(data) > 0:
        first_item = data[0]
        if isinstance(first_item, dict):
            region_info = {
                'region': first_item.get('region'),
                'shortname': first_item.get('shortname'),
                'regionid': first_item.get('regionid'),
                'dnoregion': first_item.get('dnoregion')
            }
    
    # Return full postcode and region info for partner's Streamlit components
    return Response({"data": data, "postcode": postcode, **region_info})
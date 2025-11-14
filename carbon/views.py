from django.shortcuts import render

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
    return postcode

@api_view(["GET"])
def regional_history_7d(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_seven_day_history(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    return Response({"data": data})

@api_view(["GET"])
def regional_current_30m(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_current_30_min_forecast(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    return Response({"data": data})

@api_view(["GET"])
def regional_forecast_48h(request):
    try:
        postcode = _get_postcode_from_request(request)
        data = get_48h_forecast(postcode=postcode)
    except ValueError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
    except CarbonIntensityError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
    
    return Response({"data": data})
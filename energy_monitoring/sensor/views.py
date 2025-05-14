from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import SensorData, Appliance, ScenarioSummary
from .serializers import SensorDataSerializer
from django.shortcuts import render

@api_view(['POST'])
def sensor_data(request):
    voltage = request.data.get('voltage')
    current = request.data.get('current')
    power = request.data.get('power')
    power_factor = request.data.get('power_factor')
    temperature = request.data.get('temperature')
    humidity = request.data.get('humidity')
    device_status = request.data.get('device_status')

    # Chỉ yêu cầu voltage bắt buộc
    if voltage is None:
        return Response({'error': 'Missing required field: voltage'}, status=status.HTTP_400_BAD_REQUEST)

    # Cho phép current, power là 0.0 khi device_status = "off"
    if device_status != "off" and not all([current, power,power_factor]):
        return Response({'error': 'Missing required fields: current, power, power_factor'}, status=status.HTTP_400_BAD_REQUEST)

    sensor_data = SensorData(
        voltage=float(voltage) if voltage is not None else 0.0,
        current=float(current) if current is not None else 0.0,
        power=float(power) if power is not None else 0.0,
        power_factor=float(power_factor) if power_factor is not None else 0.0,
        temperature=float(temperature) if temperature else None,
        humidity=float(humidity) if humidity else None,
        device_status=device_status
    )
    sensor_data.save()
    return Response({'message': 'Data received and saved'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_sensor_data(request):
    data = SensorData.objects.all().order_by('-timestamp')[:10]
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_usage_time(request):
    on_records = SensorData.objects.filter(device_status="on").count()
    total_seconds = on_records * 300
    total_hours = total_seconds / 3600.0
    return Response({
        'total_usage_hours': round(total_hours, 2),
        'total_usage_minutes': round(total_seconds / 60.0, 2)
    })

def sensor_data_view(request):
    return render(request, 'sensor_data.html')
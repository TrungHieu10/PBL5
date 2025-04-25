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
    temperature = request.data.get('temperature')
    humidity = request.data.get('humidity')

    if not all([voltage, current, power]):
        return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    sensor_data = SensorData(
        voltage=float(voltage),
        current=float(current),
        power=float(power),
        temperature=float(temperature) if temperature else None,
        humidity=float(humidity) if humidity else None
    )
    sensor_data.save()
    return Response({'message': 'Data received and saved'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_sensor_data(request):
    data = SensorData.objects.all().order_by('-timestamp')[:10]
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)

def sensor_data_view(request):
    return render(request, 'sensor_data.html')
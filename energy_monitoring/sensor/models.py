from django.db import models

class Appliance(models.Model):
    appliance_id = models.IntegerField(primary_key=True)
    appliance_name = models.CharField(max_length=15)
    power_rating_w = models.IntegerField()

    class Meta:
        db_table = 'appliances_table'
        managed = False

class SensorData(models.Model):
    id = models.AutoField(primary_key=True)
    voltage = models.FloatField()
    current = models.FloatField()
    power = models.FloatField()
    power_factor = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    device_status = models.CharField(max_length=10, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        db_table = 'sensor_sensordata'  
        managed = False  

class ScenarioSummary(models.Model):
    scenario_id = models.AutoField(primary_key=True)
    appliance = models.ForeignKey(Appliance, on_delete=models.CASCADE)
    time_slot = models.CharField(max_length=9)
    power_consumed_w = models.IntegerField()
    duration_hrs = models.IntegerField()
    scenario_type = models.CharField(max_length=8)
    reason_for_abnormality = models.CharField(max_length=40)

    class Meta:
        db_table = 'scenario_summary_table'
        managed = False

statusErrorsDev = ["OK","WarningMin","WarningMax","ErrorMin","ErrorMax"]
statusErrorsEnglish = [" OK"," WARNING close to min"," WARNING close to max"," ERROR under min"," ERROR over max"]
statusErrorsSpanish = [" correcta"," WARNING cercano al minimo"," WARNING cercano al maximo"," ERROR menor al minimo"," ERROR mayor al maximo"]

statusErrors = statusErrorsEnglish
class attribute:
  def __init__(self, name, value, minValue="NA", maxValue="NA", earlyWarningMin="NA", earlyWarningMax="NA"):
    self.name = name
    self.value = value
    self.minValue = minValue
    self.maxValue = maxValue
    self.earlyWarningMax = earlyWarningMax
    self.earlyWarningMin = earlyWarningMin

  def isMaxValueReached(self):
    if(self.maxValue == "NA"):
      return False
    return(self.value > self.maxValue)
  def isMinValueReached(self):
    if(self.minValue == "NA"):
      return False
    return(self.value < self.minValue)

  def isValueInEarlyWarningMax(self):
    if(self.earlyWarningMax == "NA"):
      return False
    return(self.value >= self.earlyWarningMax)
  def isValueInEarlyWarningMin(self):
    if(self.earlyWarningMin == "NA"):
      return False
    return(self.value <= self.earlyWarningMin)

  def getStatus(self):
    status = 0
    status += int(self.isValueInEarlyWarningMin())*0b10
    status += int(self.isValueInEarlyWarningMax())*0b100
    status += int(self.isMinValueReached())       *0b1000
    status += int(self.isMaxValueReached())       *0b10000
    return status
      
    
class battery:
  def __init__(self, temperature, stateOfCharge, chargeRate):
    temperatureObject = attribute("temperature",temperature,0,45,4,41)
    stateOfChargeObject = attribute("stateOfCharge",stateOfCharge,20,80,24,76)
    chargeRateObject = attribute("chargeRate",chargeRate,"NA",0.8,earlyWarningMax=0.76)
    self.attributes = {"temperature" : temperatureObject, "stateOfCharge" : stateOfChargeObject, "chargeRate" : chargeRateObject}
  
  def printAttributeStatus(self):
    attributeStatus = {}
    for attribute in self.attributes:
      print( attribute + statusErrors[ len( bin(self.attributes[attribute].getStatus()) ) - 3] )
    return attributeStatus


  def isBatteryOK(self):
    errorDetected = False
    for attribute in self.attributes:
      errorDetected |= bool( int( self.attributes[attribute].getStatus()/8) )

    return not errorDetected

def test_battery(temperature, stateOfCharge, charge_rate):
  battery_to_test = battery(temperature,stateOfCharge, charge_rate)
  batteryStatus = battery_to_test.isBatteryOK()
  # if(batteryStatus == False):
  battery_to_test.printAttributeStatus()
  return batteryStatus

if __name__ == '__main__':
  print( "########### Test everything valid")
  assert(test_battery(25, 70, 0.7) is True)

  print( "########### Test temperature under limit")
  assert(test_battery(-2, 70, 0.7) is False)
  print( "########### Test temperature over limit")
  assert(test_battery(50, 70, 0.7) is False)
  print( "########### Test temperature close under limit")
  assert(test_battery(2, 70, 0.7) is True)
  print( "########### Test temperature close over limit")
  assert(test_battery(41, 70, 0.7) is True)

  print( "########### Test State of charge under limit")
  assert(test_battery(25, 10, 0.7) is False)
  print( "########### Test State of charge over limit")
  assert(test_battery(25, 90, 0.7) is False)
  print( "########### Test State of charge close under limit")
  assert(test_battery(25, 21, 0.7) is True)
  print( "########### Test State of charge close over limit")
  assert(test_battery(25, 79, 0.7) is True)

  print( "########### Test Charge rate over limit")
  assert(test_battery(25, 70, 0.81) is False)
  print( "########### Test Charge rate close over limit")
  assert(test_battery(25, 70, 0.79) is True)

  print( "########### Test everything invalid")
  assert(test_battery(-10, 5, 0.9) is False)



    
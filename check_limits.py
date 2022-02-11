def isUpLimitNotReached(value, max_value):
  if(max_value == "NA" or value <= max_value):
    return True
  else:
    return False

def isDownLimitNotReached(value, min_value):
  if(min_value == "NA" or value >= min_value):
    return True
  else:
    return False
class battery:
  def __init__(self, temperature, stateOfCharge, chargeRate):
    self.attributes = {"temperature" : temperature, "stateOfCharge" : stateOfCharge, "chargeRate" : chargeRate}

  MIN_VALUES = {"temperature":0,"stateOfCharge":20,"chargeRate":"NA"}
  MAX_VALUES = {"temperature":45,"stateOfCharge":80,"chargeRate":0.8}
  

  def isBatteryOK(self):
    batteryOK = True
    for attribute in self.attributes:
      batteryOK &= isUpLimitNotReached(self.attributes[attribute],self.MAX_VALUES[attribute])
      batteryOK &= isDownLimitNotReached(self.attributes[attribute],self.MIN_VALUES[attribute])
    return batteryOK

def battery_is_ok(temperature, soc, charge_rate):
  battery_to_test = battery(temperature,soc, charge_rate)
  return battery_to_test.isBatteryOK()

if __name__ == '__main__':
  #Test everything valid
  assert(battery_is_ok(25, 70, 0.7) is True)

  #Test temperature under limit
  assert(battery_is_ok(-2, 70, 0.7) is False)
  #Test temperature over limit
  assert(battery_is_ok(50, 70, 0.7) is False)

  #Test State of charge under limit
  assert(battery_is_ok(25, 10, 0.7) is False)
  #Test State of charge over limit
  assert(battery_is_ok(25, 90, 0.7) is False)

  #Test Charge rate over limit
  assert(battery_is_ok(25, 70, 0.81) is False)

  #Test everything invalid
  assert(battery_is_ok(-10, 5, 0.9) is False)



    
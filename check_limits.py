def value_is_out_of_umbrall(value,min_value="NA",max_value="NA"):
  validValue = False
  if(min_value != "NA"):
    if(value<min_value):
      validValue = True
  if(max_value != "NA"):
    if(value>max_value):
      validValue = True
  return validValue

def outOfRangeAlert(reasons):
  if(reasons):
    messagetoPrint = ""
    number_of_reasons = len(reasons)
    if(number_of_reasons==1):
      messagetoPrint += reasons[0] + " is out of range"
    else:
      for i,reason in enumerate(reasons):
        if(i+1 == number_of_reasons):
          messagetoPrint = messagetoPrint[:-2]
          messagetoPrint += " and "+reason
        else:
          messagetoPrint += reason + ", "
      messagetoPrint += " are out of range"
    print(messagetoPrint)

def battery_is_ok(temperature, soc, charge_rate):
  invalidValues = []

  if(value_is_out_of_umbrall(temperature,0,45)):
    invalidValues.append("Temperature")
  if(value_is_out_of_umbrall(soc,20,80)):
    invalidValues.append("State of charge")
  if(value_is_out_of_umbrall(charge_rate,max_value=0.8)):
    invalidValues.append("Charge rate")

  if(invalidValues):
    outOfRangeAlert(invalidValues)
    return False

  return True

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
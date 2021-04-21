from labjack import ljm
import sys

MAX_REQ = 30

handle = ljm.openS("ANY", "ANY", "ANY")
info = ljm.getHandleInfo(handle)
print("Opened a LabJack with Device type: %i, Connection type: %i,\n"
      "Serial number: %i, IP address: %s, Port: %i,\nMax bytes per MB: %i" %
      (info[0], info[1], info[2], ljm.numberToIP(info[3]), info[4], info[5]))

deviceType = info[0]


#Stream Config
scanListNames = ["AIN0", "AIN1"]
numAddress = len(scanListNames)
scanList = ljm.namesToAddresses(numAddress, scanListNames)[0]
scanRate = 10000 # Scan Rate 10kHz
scansPerRead = int(scanRate/2)

try:
      # For Labjact T7
      # Trigerred Stream disables
      ljm.eWriteName(handle, "STREAM_TRIGGER_INDEX",0)

      # Internally clocked Stream
      ljm.eWriteName(handle, "STREAM_CLOCK_SOURCE", 0)

      # All negative channels are single-ended, AIN0 and AIN1 ranges are
      # +/-10 V, stream settling is 0 (default) and stream resolution index
      # is 0 (default).

      anNames = ["AIN_ALL_NEGATIVE_CH", "AIN0_RANGE", "AIN1_RANGE", "STREAM_SETTLING_US", "STREAM_RESOLUTION_INDEX"]
      anValues = [ljm.constants.GND, 10.0, 10.0, 0, 0]
      numFrame = len(anNames)
      ljm.eWriteNames(handle, numFrame, anNames, anValues)

      # Initiate stream
      scanRate = ljm.eStreamStart(handle, scansPerRead, numAddress, scanList, scanRate)
      print("\nStream started with a scan rate of %i Hz." % scanRate)
      i = 0
      while i<=MAX_REQ:
            read = ljm.eStreamRead(handle)
            anData = read[0]
            scan = len(anData)/numAddress
            print(numAddress)
            
            strmVal = ""
            for j in range (numAddress):
                  strmVal += "Reading: %s = %0.5f  " % (scanListNames[j], anData[j])
            print ("Scan %i of  %i: %s" % (i,scan,strmVal))
            


            i+=1
except ljm.LJMError:
    ljme = sys.exc_info()[1]
    print(ljme)
except Exception:
    e = sys.exc_info()[1]
    print(e)

try:
    print("\nStop Stream")
    ljm.eStreamStop(handle)
except ljm.LJMError:
    ljme = sys.exc_info()[1]
    print(ljme)
except Exception:
    e = sys.exc_info()[1]
    print(e)

# Close handle
ljm.close(handle)

            






import datetime
import time

epoch_time = 1686060539
date_conv = datetime.datetime.fromtimestamp(epoch_time)
print(date_conv.strftime('%d-%m-%Y'))
print(int(time.time()))

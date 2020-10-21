from django.test import TestCase
import time,datetime
# Create your tests here.

# now_time = datetime.datetime.now()
now_time = time.strftime('%Y-%m-%d %H:%M:%S ',time.localtime(time.time()))
# print(time)
print(now_time)

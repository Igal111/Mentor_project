import csv


def ip_into_lst(IP):
    ip = [int(x) for x in IP.split(".")]
    return ip


def ip_into_number(IP):
  IP = ip_into_lst(IP)
  IP[0] *= 16777216
  IP[1] *= 65536
  IP[2] *= 256
  ip = IP[0] + IP[1] + IP[2] + IP[3]
  return int(ip)


def num_to_IP(ip_num):
   num1 = int(ip_num / 16777216) % 256
   num2 = int(ip_num / 65536) % 256
   num3 = int(ip_num / 256) % 256
   num4 = int(ip_num) % 256
   return '%(num1)s.%(num2)s.%(num3)s.%(num4)s' % locals()


def ip_range_check(range_start, ip, range_end):
   if range_start <= ip and range_end >= ip:
     print("this ip is in your range")
   else:
     print("this ip isn't in your range")


def read_csv(path):
   with open(path, newline = "\n") as file:
     reader = csv.reader(file)
     data = list(reader)
   return data


def write_csv(data, path = "result1.csv"):
   with open(path, "a", newline = "\n") as file:
     writer = csv.writer(file)
     for row in data:
       writer.writerow(row)


def get_ip_location(ip_num, ip_location):
   ip_location = ip_location[1:]
   for row in ip_location:
    if ip_num >= int(row[0]) and ip_num <= int(row[1]):
      return row[3]


def get_ip_range(ip, ip_ranges):
   ip_ranges = ip_ranges[1:]
   for row in ip_ranges:
     ip_start = int(row[-2])
     ip_end = int(row[-1])
     if ip >= ip_start and ip <= ip_end:
       return row[2]


ip_ranges = read_csv("private_ip_ranges.csv")
ip_location = read_csv("ip_location_data.csv")
data = read_csv("connections.csv")
data = data[1:]
result = ['Src IP'	,'source ip range',	'source internet location',	'Dest IP'	,'dest ip range'	,'dest internet location',	'Protocol'	,'Count',	'Unsecured']

for i, row in enumerate(data):
# Helps to track the progres of the progrem
   print(f'  {i} / {len(data)}')
   src_ip = row[0]
   dst_ip = row[1]
   src_ip_num = ip_into_number(src_ip)
   src_ip_range = get_ip_range(src_ip_num, ip_ranges)
   dst_ip_num = ip_into_number(dst_ip)
   dst_ip_range = get_ip_range(dst_ip_num, ip_ranges)
  
   if src_ip_range == 'Not In Private IP Address Range':
     src_ip_location = get_ip_location(src_ip_num, ip_location)
   else:
     src_ip_location = ''
  
   if dst_ip_range == 'Not In Private IP Address Range':
     dst_ip_location = get_ip_location(dst_ip_num, ip_location)
   else:
     dst_ip_location = ''
    
   new_row = [src_ip, src_ip_range, src_ip_location, dst_ip, dst_ip_range, dst_ip_location] + row[2:]
   result.append(new_row)

write_csv(result)
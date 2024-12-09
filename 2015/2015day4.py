import hashlib

def get_password(key):
  num = 1

  while True:
    hash = hashlib.md5((key + str(num)).encode())
    
    if hash.hexdigest()[:6] == "000000":
      break
    
    num += 1

  return num

print(get_password("bgvyzdsv"))


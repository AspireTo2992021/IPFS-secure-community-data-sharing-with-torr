import hashlib
import datetime
transaction = {"address" :"b'65ZgcwtmdcCxDAKTCwSZu7miP9F2cuEuy2ewtaKrPj1AXrbPeL1DEwb'" , "key" : "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQ//4vgRjkBGGe/gwbD6sipyTJ\ne+lG8Y+W/whJQtLPcWaKQ5tp+9AgvG/aiYR/YGHNyXWqPSrBOYFrYiRStykw4Mrp\nKjft3E1Yo+Ly6Jf+8BYYslh24HW4gvejwu2QiLtdrcJ9HAbqXZ0ENK7msGjjDmQk\neP5knWmobZDA8hvuawIDAQAB\n-----END PUBLIC KEY-----"}
timestamp =   str(datetime.datetime.now())
transaction=[]
print(timestamp)
def pow():        
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256((str(transaction)+timestamp+str(new_proof)).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof , hash_operation

print(pow())
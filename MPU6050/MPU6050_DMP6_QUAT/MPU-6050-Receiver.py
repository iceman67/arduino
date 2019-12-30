import time
import serial

# https://github.com/ElectronicCats/mpu6050/blob/master/examples/MPU6050_DMP6/MPU6050_DMP6.ino
# http://blog.naver.com/PostView.nhn?blogId=ysahn2k&logNo=221410391235&parentCategoryNo=&categoryNo=47&viewDate=&isShowPopularPosts=false&from=postView

# MPU-6050은100 HZ 로 동작되고 있음

import argparse
def parse_args():
    # Parse command line arguments
    ap = argparse.ArgumentParser(description="MPU-6050 data receiver")
    ap.add_argument("-i", "--input", required=True,
                    help="input channel")
    return vars(ap.parse_args())


def maketuple(variables, names):
  return tuple(variables[n] for n in names)

def getYRP(response):
    getGyro = response.split('\t')
    x = float(getGyro[1])
    y = float(getGyro[2])
    z = float(getGyro[3])

    yprTuple = maketuple(vars(), 'x y z'.split())
    return yprTuple

def getQUAT(response):
    getQuat = response.split('\t')
    if (len(getQuat) == 5):
        if type(float(getQuat[1])) is float:
             w = float(getQuat[1])
        else:
            print('Data is not in float and hence marked to zero')
            getQuat[1] = 0.0
            w = float(getQuat[1])

        if type(float(getQuat[2])) is float:
             x = float(getQuat[2])
        else:
            print('Data is not in float and hence marked to zero')
            getQuat[2] = 0.0
            x= float(getQuat[2])

        if type(float(getQuat[3])) is float:
             y = float(getQuat[3])
        else:
            print('Data is not in float and hence marked to zero')
            getQuat[3] = 0.0
            y= float(getQuat[3])

        if type(float(getQuat[4])) is float:
             z = float(getQuat[4])
        else:
            print('Data is not in fl oat and hence marked to zero')
            getQuat[4] = 0.0
            z= float(getQuat[4])

    outputQuat = "{} - {}".format(x,y)

    if x < 0:
        print("Turn off the light")
    elif x >0:
        print("Turn on the light")

    print (outputQuat)
    quatTuple = maketuple(vars(), 'w x y z'.split())
    return quatTuple


def main(args):
    ser = serial.Serial(
    #   port='COM16',
       port=args["input"],
       baudrate=115200,
    )

    if ser.is_open == True:
       ser.close()

    ser.open()
    while True:
       while ser.inWaiting() == 0:
           pass
       response = ser.readline()
       response = str(response, encoding="utf-8")
       print("read data: " + response)
       if response.startswith('Send'):
          ser.write(str.encode('r'))
       gyroTuple = []
       if response.startswith('ypr'):
          print (getYRP(response))
       elif response.startswith('quat'):
          print(getQUAT(response))

       time.sleep(0.0001)


if __name__ == '__main__':

    args = parse_args()

    main(args)
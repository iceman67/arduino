import time
import serial
import tkinter as tk # Python3

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

x = 0
y = 0
z = 0
w = 0
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

# 측정값에서 원 이동량을 결정하는 함수
def movement(val):
    # 측정값에서 이동량을 결정
    m_val = 0
    if val > 0.2 :
        m_val = 2
    elif val > 0.1 :
        m_val = 1
    elif val < -0.2 :
        m_val = -2
    elif val < -0.1 :
        m_val = -1
    # 결과 반환
    return m_val


def check_acc(x, y):
    # x 방향 데이터 얻음
    x_acc =  x * -1
    # y 방향 데이터 얻음
    y_acc = y
    # 결과를 리스트로 반환
    return [movement(x_acc), movement(y_acc)]

def draw():
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
          cTuple = getQUAT(response)
          # 이동량 얻음
          diff = check_acc(cTuple[1], cTuple[2])
          # 이동량에 따라 움직임
          c.move(cc, diff[0], diff[1])
          #time.sleep(0.0001)
       root.after(50, draw)

if __name__ == '__main__':
    # Tk 객체 인스턴스 생성
    root = tk.Tk()

    # Canvas 객체 인스턴스 생성
    # 폭: 200, 높이: 200
    c = tk.Canvas(root, width=500, height=500)
    # 캔버스 배치
    c.pack()

    # 원 작성
    # 좌표 (200, 200)에서 (220, 220), 색: 녹색
    cc = c.create_oval(200, 200, 220, 220, fill='green')
    args = parse_args()
    ser = serial.Serial(
        #   port='COM16',
        port=args["input"],
        baudrate=115200,
    )

    if ser.is_open == True:
        ser.close()
    ser.open()

    draw()

    # root 표시
    root.mainloop()
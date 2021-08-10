"""
-------------------------------------------------
   Description :
   Author :       Jing
   E-mail:        jliu4@heygears.com
   date：        2021/8/9 17:27

-------------------------------------------------
"""
import  time
import argparse
from PIL import Image
import struct
import os

class Data_Handler():

    @staticmethod
    def HexString( bl):
        # warnings.warn(" turn to fixture, deprecated", DeprecationWarning)
        s = ""
        blen = len(bl)
        for i in range(0, blen):
            if i == blen - 1:
                s += hex(bl[i])
            else:
                s += hex(bl[i]) + " "
        return s

    @staticmethod
    def bytestoint(buff):
        # warnings.warn(" turn to fixture, deprecated", DeprecationWarning)
        blist = []
        for e in buff:
            blist.append(int.from_bytes(e, byteorder='big', signed=False))
        return blist

    @staticmethod
    def HexToBytes(dstr):
        # warnings.warn(" turn to fixture, deprecated", DeprecationWarning)
        sl=dstr.split(" ")
        bl=[]
        if len(sl)>0:
            for e in sl:
                bl.append(int(e,16))
        return bl

    '''
    协议通讯状态解析
    '''

    @staticmethod
    def GetRealState( b):
        s=""
        if b==0x00:
            s="正常"
        elif b==0xff:
            s="异常"
        else:
            s="其他异常"+hex(b)
        return s

    @staticmethod
    def GetRealInt( bl):
        b = (bl[1]//16)*16*16*16+(bl[1]%16)*16*16+(bl[0]//16)*16+bl[0] % 16
        return b

    '''
    数据值获取：例如光强值，温度值
    '''

    @staticmethod
    def GetRealValue(sl):
        # warnings.warn(" turn to fixture, deprecated", DeprecationWarning)
        slen=len(sl)
        maxv=0.0
        minv=0.0
        sumv=0.0
        for i in range(0,slen):
            if i==0:
                maxv=float(sl[i])
                minv=float(sl[i])
            else:
                if float(sl[i])>maxv:
                    maxv=float(sl[i])
                if float(sl[i])<minv:
                    minv=float(sl[i])
            sumv+=float(sl[i])
        ev=(sumv-maxv-minv)//(slen-2)
        return ev

    @staticmethod
    def GetTimeSmap(uarttime):
        # warnings.warn(" turn to fixture，is deprecated", DeprecationWarning)
        t = time.time()
        tmp = int(round(t * 1000))
        rtmp = 0
        try:
            rtmp = tmp-uarttime
        except Exception as e:
            print(str(e))
        return str(rtmp)

    @staticmethod
    def Get_imgfile():
        fpath = os.getcwd()
        dlist = []
        for root, dirs, files in os.walk(fpath):
            for filename in files:
                if ".png" in filename or ".bmp" in filename or ".jpg" in filename:
                    if root == fpath:
                        fullname = os.path.join(root, filename)
                        dlist.append(fullname)
        print(dlist)
        return dlist

    @staticmethod
    def img2fb(imgpath, spath):
        '''

             :param imgpath: 图像原始路径
             :param spath:  framebuffer 输出路径
             :return:  none
             '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-i' , '--input' , dest='img_in'    , metavar='IMAGE' , help="image to handle" , default=imgpath)
        parser.add_argument('-o' , '--output', dest='img_out'   , metavar='IMAGE' , help="image to fb"     , default=spath)
        parser.add_argument('-bw', '--width' , dest='buf_width' , metavar='WIDTH' , help="width of buffer" , type=int)
        parser.add_argument('-bh', '--height', dest='buf_height', metavar='HEIGHT', help="height of buffer", type=int)
        parser.add_argument('-f' , '--format', dest='format'    , metavar='FORMAT', help="format,RGB,BGR,ARGB...",default='RGB')

        args = parser.parse_args()
        args.format = args.format.upper()

        im = Image.open(args.img_in).convert("RGBA")
        w, h = im.size

        pixels = {'A': 0, 'R': 0, 'G': 0, 'B': 0}

        #if not define the size of framebuffer,use the size of image
        if args.buf_width == None:
            args.buf_width = w
        if args.buf_height == None:
            args.buf_height = h

        print('Image:',args.img_in,' ',w,'X',h,im.mode)
        print('FrameBuffer:',args.buf_width,'X',args.buf_height,args.format)
        #if the size of image larger than than the framebuffer,cut it
        if(w > args.buf_width):
            w = args.buf_width
            print('cut the Image width to',args.buf_width)

        if(h > args.buf_width):
            h = args.buf_height
            print('cut the Image height to',args.buf_width)


        with open(args.img_out, 'wb') as f:
            for j in range(0,h):
                for i in range(0,w):
                    pixels['R'],pixels['G'],pixels['B'],pixels['A']=im.getpixel((i,j))
                    for n in args.format:
                        f.write(struct.pack('B',pixels[n]))
                #if the image smaller than the framebuffer,fill in 0
                for i in range(w,args.buf_width):
                    for n in args.format:
                        f.write(struct.pack('B',0))

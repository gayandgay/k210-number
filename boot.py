# object detector boot.py
# generated by maixhub.com

import sensor, image, lcd, time
import KPU as kpu
import gc, sys
# from machine import UART
# from fpioa_manager import fm
import Uart
import time

def lcd_show_except(e):
    import uio
    err_str = uio.StringIO()
    sys.print_exception(e, err_str)
    err_str = err_str.getvalue()
    img = image.Image(size=(224,224))
    img.draw_string(0, 10, err_str, scale=1, color=(0xff,0x00,0x00))
    lcd.display(img)

def main(anchors, labels = None,  sensor_window=(224, 224), model_addr="/sd/models/m.kmodel",lcd_rotation=0, sensor_hmirror=False, sensor_vflip=False, modelflag = 0):
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.set_windowing(sensor_window)
    sensor.set_hmirror(sensor_hmirror)
    sensor.set_vflip(sensor_vflip)
    sensor.run(1)

    lcd.init(type=1)
    lcd.rotation(lcd_rotation)
    lcd.clear(lcd.WHITE)

    Uart.UartInit()
    # fm.register(24, fm.fpioa.UART1_TX, force=True)
    # fm.register(25, fm.fpioa.UART1_RX, force=True)
    # fm.register(22, fm.fpioa.UART2_TX, force=True)
    # fm.register(23, fm.fpioa.UART2_RX, force=True)

    # uart_A = UART(UART.UART1, 115200, 8, 0, 1, timeout=1000, read_buf_len=4096)
    # uart_B = UART(UART.UART2, 115200, 8, 0, 1, timeout=1000, read_buf_len=4096)

    if not labels:
        with open('labels.txt','r') as f:
            exec(f.read())
    if not labels:
        print("no labels.txt")
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "no labels.txt", color=(255, 0, 0), scale=2)
        lcd.display(img)
        return 1
    try:
        img = image.Image("startup.jpg")
        lcd.display(img)
    except Exception:
        img = image.Image(size=(320, 240))
        img.draw_string(90, 110, "loading model...", color=(255, 255, 255), scale=2)
        lcd.display(img)

    task = kpu.load(model_addr)
    kpu.init_yolo2(task, 0.5, 0.3, 5, anchors) # threshold:[0,1], nms_value: [0, 1]
    try:
        while 1:
            img = sensor.snapshot()
            t = time.ticks_ms()
            objects = kpu.run_yolo2(task, img)
            t = time.ticks_ms() - t
            if objects:
                for obj in objects:
                    pos = obj.rect()
                    img.draw_rectangle(pos)
                    img.draw_string(pos[0], pos[1], "%s : %.2f" %(labels[obj.classid()], obj.value()), scale=2, color=(255, 0, 0))
                    if labels[obj.classid()] != "netLine" :
                        Uart.UartSend(labels[obj.classid()],pos[0])
                    else :
                        Uart.UartSend(labels[obj.classid()],pos[1])
                    # Uart.UartSend(labels[obj.classid()])
                    #time.sleep(0.001)
            img.draw_string(0, 200, "t:%dms" %(t), scale=2, color=(255, 0, 0))
            lcd.display(img)
    except Exception as e:
        raise e
    finally:
        kpu.deinit(task)


if __name__ == "__main__":
    try:
        #labels = ['1', '2', '3', '4', '5', '6', '7', '8']
        #anchors = [1.40625, 1.8125000000000002, 5.09375, 5.28125, 3.46875, 3.8124999999999996, 2.0, 2.3125, 2.71875, 2.90625]
        #main(anchors = anchors, labels=labels, model_addr=0x300000, lcd_rotation=2, sensor_window=(224, 224))
        labels = ['1', '2', '3', '4', '5', '6', '7', '8']
        anchors = [2.16, 2.84, 0.55, 0.87, 3.05, 3.16, 1.13, 1.53, 1.91, 1.97]
        main(anchors = anchors, labels=labels, model_addr="/sd/models/m2.kmodel", lcd_rotation=2, sensor_window=(224, 224))
    except Exception as e:
        sys.print_exception(e)
        lcd_show_except(e)
    finally:
        gc.collect()
from machine import UART
from fpioa_manager import fm

def UartInit():
    fm.register(24, fm.fpioa.UART1_TX, force=True)
    fm.register(25, fm.fpioa.UART1_RX, force=True)
    # fm.register(22, fm.fpioa.UART2_TX, force=True)
    # fm.register(23, fm.fpioa.UART2_RX, force=True)

    
    # uart_B = UART(UART.UART2, 115200, 8, 0, 1, timeout=1000, read_buf_len=4096)

def UartSend(label, position):
    uart_A = UART(UART.UART1, 115200, 8, 0, 1, timeout=1000, read_buf_len=4096)
    # uart_A.write(text)
    uart_A.write(f'{position}:{label}\n'.encode('utf-8'))
import sys
import glob
import serial

std_speeds = ['1843200', '921600', '460800', '230400', '115200', '57600', '38400', '19200', '9600', '4800', '2400', '1200', '600', '300', '150', '100', '75', '50'] #Скорость COM порта
paritys = ['N', 'E', 'O']   #Бит четности
stopbitss = [1, 2]             #Количество стоп-бит
bite_size = 8               #Биты данных
t_out = 1                   #Таймаут в секундах, должен быть больше 1с
flag1=0                     #Флаг для остановки программы, устанавливается в 1, если найдена сигнатура
reading_bytes = 10          #Количество байт для чтения после открытия порта
keyword=b'\x00\x00\x00'     #!Сигнатура для поиска
cmd = b'\x00\x34\x65'       #!Команда перед началом приема
ser = serial.Serial()

def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def parametersPort(ser):
    try:
        for stop_bit in stopbitss:
            for parit in paritys:
                for com_speed in std_speeds:
                    ser.close()
                    ser.baudrate = com_speed
                    ser.timeout = t_out
                    ser.bytesize = bite_size
                    ser.parity = parit
                    ser.stopbits = stop_bit
                    ser.open()
                    # ser.write(cmd)                                       #!Раскомментировать при необходимости отправки команды в устройство для инициализации связи
                    message_b = ser.read(reading_bytes)
                    if flag1 == 1:
                        break
                    if message_b:
                        print('\nRAW data on ' + ser.port + ', ' + com_speed + ', ' + str(
                            ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits) + ':')
                        print('---------------------')
                        print(message_b)
                        print('---------------------')
                        try:
                            if keyword in message_b:
                                print('\n\033[0;33mСигнатура ', end='')  # желтый цвет текста
                                print(keyword, end='')
                                print(
                                    ' найдена при следующих настройках: \n' + ser.port + ', ' + com_speed + ', ' + str(
                                        ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits))
                                print('\x1b[0m')
                                ser.close()
                                flag1 = 1
                                break
                            else:
                                ser.close()
                        except:
                            print('error decode')
                            print('---------------------')
                            ser.close()
                    else:
                        print('timeout on ' + ser.port + ', ' + com_speed + ', ' + str(
                            ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits))
                        print('---------------------')
                        ser.close()
        if flag1 == 0:
            print('Поиск завершен, сигнатура не найдена')
    except serial.SerialException:
        print('Ошибка при открытии порта ' + ser.port)
        sys.exit()



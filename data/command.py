class Command:
    BEGIN = b"BEGIN\n"
    END = b"END\n"

    DISTANT_SENSOR_READ = b"d\n"
    LINE_SENSOR_READ = b"l\n"
    LIGHT_SENSOR_READ = b"i\n"
    TEMP_SENSOR_READ = b"t\n"

    R = "r"
    G = "g"
    B = "b"

    LASER_HIGH = b'z1\n'
    LASER_LOW = b'z0\n'

    LED_LOW = b's0\n'
    LED_HIGH = b's1\n'



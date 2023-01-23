from machine import Pin, ADC
import time

led_pins = [
    Pin(0, Pin.OUT),
    Pin(1, Pin.OUT),
]

trigger_pin = Pin(14, Pin.OUT)
echo_pin = Pin(15, Pin.IN)
value = ADC(4)


def measure_distance():
    """
        Meet de afstand met de SR04
    """
    trigger_pin.low()
    time.sleep_us(2)
    trigger_pin.high()
    time.sleep_us(5)
    trigger_pin.low()
    while echo_pin.value() == 0:
        pulse_start = time.ticks_us()
    while echo_pin.value() == 1:
        pulse_end = time.ticks_us()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17165 / 1000000
    distance = round(distance, 0)
    # implementeer deze functie

    return distance


def display_distance(distance):
    """
        Laat de afstand d.m.v. de leds zien.
        1 led =  10 cm
        2 leds = 50 cm
    """

    if distance <= 10:
        led_pins[1].value(1)
        print(1)
        time.sleep(1)
        led_pins[1].value(0)


        time.sleep(1)
    elif distance <= 50:
        led_pins[0].value(1)
        print(0)
        time.sleep(1)
        led_pins[0].value(0)
        time.sleep(1)

while True:
    distance = measure_distance()
    display_distance(distance)
    time.sleep_ms(100)
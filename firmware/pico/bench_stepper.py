"""Off-machine bench tester: Pi Pico (MicroPython) -> TB6600 -> 17HS15-1584S-MG50.

Use it to prove the motor, gearbox, pulleys and belt tension BEFORE opening the spindle head.
Optional: an AS5600 on I2C0 reads the output angle (stick a diametric magnet on the TopGear face).

Wiring (TB6600 common-anode, 3.3 V logic works on most units):
  TB6600 PUL+, DIR+, ENA+  -> Pico 3V3 (pin 36)
  TB6600 PUL-  -> GP2   DIR- -> GP3   ENA- -> GP4  (GP4 LOW = TB6600 'enable' input active = motor FREE)
  TB6600 A+/A-/B+/B- -> motor coils (check pairs with a meter, ~1-3 ohm)
  TB6600 VCC/GND -> 12-24 V DC supply (NOT from the Carvera)
  TB6600 DIP: 1.5 A peak, 8 microsteps (set MICROSTEP below to match)
  AS5600 (optional): VCC 3V3, GND, SDA GP0, SCL GP1, DIR->GND
"""
from machine import Pin, I2C
import time

MICROSTEP = 8
GEAR = 50                    # 50:1 planetary
STEPS_PER_REV_OUT = 200 * MICROSTEP * GEAR

pul, dirp, ena = Pin(2, Pin.OUT, value=1), Pin(3, Pin.OUT, value=1), Pin(4, Pin.OUT, value=1)

try:
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
    HAS_ENC = 0x36 in i2c.scan()
except Exception:
    HAS_ENC = False

def angle():
    if not HAS_ENC:
        return None
    hi, lo = i2c.readfrom_mem(0x36, 0x0E, 2)
    return ((hi & 0x0F) << 8 | lo) * 360 / 4096

def move(deg_out, rpm_out=6):
    """Rotate the gearbox OUTPUT by deg_out degrees at rpm_out."""
    steps = int(abs(deg_out) / 360 * STEPS_PER_REV_OUT)
    dirp.value(0 if deg_out > 0 else 1)
    half = max(20, int(1_000_000 / (rpm_out / 60 * STEPS_PER_REV_OUT) / 2))
    ena.value(1)  # ENA opto off -> driver energised
    for _ in range(steps):
        pul.value(0); time.sleep_us(half); pul.value(1); time.sleep_us(half)

def cycle(deg=90, n=20, rpm=6, dwell=0.3):
    """Clamp/unclamp style back-and-forth. Prints encoder angle to check backlash/slip."""
    for i in range(n):
        a0 = angle(); move(deg, rpm); time.sleep(dwell)
        a1 = angle(); move(-deg, rpm); time.sleep(dwell)
        print(i, "angle start", a0, "after +move", a1, "end", angle())
    ena.value(0)  # release motor

if __name__ == "__main__":
    print("encoder:", HAS_ENC)
    cycle()

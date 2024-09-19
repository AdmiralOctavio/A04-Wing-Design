import math
from enum import Enum


class Quantity(Enum):
    Temperature = 0,
    Pressure = 1,
    Density = 2


def get_quantity(quantity: Quantity, temperature: float, pressure: float, density: float) -> float:
    if quantity == Quantity.Temperature:
        return temperature
    elif quantity == Quantity.Pressure:
        return pressure
    elif quantity == Quantity.Density:
        return density
    else:
        return 0


def troposphere(altitude: float, quantity: Quantity) -> float:
    temperature = 288.15 - 0.0065 * altitude
    pressure = math.pow(temperature / 288.15, -9.80665 / (-0.0065 * 287)) * 101325
    density = pressure / (287 * temperature)

    return get_quantity(quantity, temperature, pressure, density)


def stratosphere(altitude: float, quantity: Quantity) -> float:
    temperature = troposphere(altitude, Quantity.Temperature)
    pressure = (math.exp(-9.80665 * (altitude - 11000) / (287 * temperature)) *
                troposphere(11000, Quantity.Pressure))
    density = pressure / (287 * temperature)

    return get_quantity(quantity, temperature, pressure, density)


def mesosphere(altitude: float, quantity: Quantity) -> float:
    temperature = stratosphere(altitude, Quantity.Temperature) + 0.001 * (altitude - 20000)
    pressure = (math.pow(temperature / troposphere(11000, Quantity.Temperature), -9.80665 / (0.001 * 287))
                * stratosphere(20000, Quantity.Pressure))
    density = pressure / (287 * temperature)

    return get_quantity(quantity, temperature, pressure, density)


def thermosphere(altitude: float, quantity: Quantity) -> float:
    temperature = mesosphere(32000, Quantity.Temperature) + 0.0028 * (altitude - 32000)
    pressure = (math.pow(temperature / mesosphere(32000, Quantity.Temperature), -9.80665 / (0.0028 * 287))
                * mesosphere(32000, Quantity.Pressure))
    density = pressure / (287 * temperature)

    return get_quantity(quantity, temperature, pressure, density)


def exosphere(altitude: float, quantity: Quantity) -> float:
    temperature = thermosphere(47000, Quantity.Temperature)
    pressure = math.exp(-9.80665 * (altitude - 47000) / (287 * temperature)) * thermosphere(47000, Quantity.Pressure)
    density = pressure / (287 * temperature)

    return get_quantity(quantity, temperature, pressure, density)


def get_quantity_at_altitude(altitude: float, quantity: Quantity, default_value: float) -> float:
    if altitude <= 11000:
        return troposphere(altitude, quantity)
    elif 11000 < altitude <= 20000:
        return stratosphere(altitude, quantity)
    elif 20000 < altitude <= 32000:
        return mesosphere(altitude, quantity)
    elif 32000 < altitude <= 47000:
        return thermosphere(altitude, quantity)
    elif 47000 < altitude:
        return exosphere(altitude, quantity)
    else:
        return default_value


def get_temperature(altitude: float) -> float:
    return get_quantity_at_altitude(altitude, Quantity.Temperature, 288.15)


def get_pressure(altitude: float) -> float:
    return get_quantity_at_altitude(altitude, Quantity.Pressure, 101325)


def get_density(altitude: float) -> float:
    return get_quantity_at_altitude(altitude, Quantity.Density, 1.225)

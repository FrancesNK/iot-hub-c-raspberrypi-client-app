/*
* IoT Hub Raspberry Pi C - Microsoft Sample Code - Copyright (c) 2017 - Licensed MIT
*/
#include "./wiring.h"

static unsigned int BMEInitMark = 0;

#if SIMULATED_DATA
int random(int min, int max)
{
    // int range = (int)(rand()) % (100 * (max - min));
    // return min + range / 100;
    return min + (rand() % (max - min));
}

int readMessage(int messageId, char *payload)
{
    int temperature = random(35, 43);
    int pulse = random(30,200);
    int DP = random (30,120);
    int SP = random (50,200);
    snprintf(payload,
             BUFFER_SIZE,
             "{ \"deviceId\": \"Raspberry Pi - C\", \"messageId\": %d, \"temperature\": %d, \"pulse\": %d, \"DP\": %d, \"SP\": %d, \"orthopedics\": %d,\"cardiology\": %d,\"respiratory\": %d,\"Severity\": %d }",
             messageId,
             temperature,
             pulse,
	     DP,
	     SP,random(0,2),random(0,2),random(0,2),random(0,4));
    //return (temperature > TEMPERATURE_ALERT) ? 1 : 0;
    return 0;
}

#else
int mask_check(int check, int mask)
{
    return (check & mask) == mask;
}

// check whether the BMEInitMark's corresponding mark bit is set, if not, try to invoke corresponding init()
int check_bme_init()
{
    // wiringPiSetup == 0 is successful
    if (mask_check(BMEInitMark, WIRINGPI_SETUP) != 1 && wiringPiSetup() != 0)
    {
        return -1;
    }
    BMEInitMark |= WIRINGPI_SETUP;

    // wiringPiSetup < 0 means error
    if (mask_check(BMEInitMark, SPI_SETUP) != 1 && wiringPiSPISetup(SPI_CHANNEL, SPI_CLOCK) < 0)
    {
        return -1;
    }
    BMEInitMark |= SPI_SETUP;

    // bme280_init == 1 is successful
    if (mask_check(BMEInitMark, BME_INIT) != 1 && bme280_init(SPI_CHANNEL) != 1)
    {
        return -1;
    }
    BMEInitMark |= BME_INIT;
    return 1;
}

// check the BMEInitMark value is equal to the (WIRINGPI_SETUP | SPI_SETUP | BME_INIT)

int readMessage(int messageId, char *payload)
{
    if (check_bme_init() != 1)
    {
        // setup failed
        return -1;
    }

    float temperature, humidity, pressure;
    if (bme280_read_sensors(&temperature, &pressure, &humidity) != 1)
    {
        return -1;
    }

    snprintf(payload,
             BUFFER_SIZE,
             "{ \"deviceId\": \"Raspberry Pi - C\", \"messageId\": %d, \"temperature\": %f, \"humidity\": %f }",
             messageId,
             temperature,
             humidity);
    return temperature > TEMPERATURE_ALERT ? 1 : 0;
}
#endif

void blinkLED()
{
    digitalWrite(LED_PIN, HIGH);
    delay(100);
    digitalWrite(LED_PIN, LOW);
}

void setupWiring()
{
    if (wiringPiSetup() == 0)
    {
        BMEInitMark |= WIRINGPI_SETUP;
    }
    pinMode(LED_PIN, OUTPUT);
}

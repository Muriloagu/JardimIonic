import spidev
import time
from libsoc import gpio
from gpio_96boards import GPIO
from dweet import Dweet

VOLUME = GPIO.gpio_id('GPIO_CS') #SENSOR VOLUME DAGUA
TEMPERATURA = GPIO.gpio_id('GPIO_CS') #SENSOR DE TEMPERATURA
SOL = GPIO.gpio_id('GPIO_CS') #SENSOR DE LUMINOSIDADE
ILUMINACAO = GPIO.gpio_id('GPIO_C') #LED
IRRIGACAO = GPIO.gpio_id('GPIO_E') #RELE - LIGADO A VALVULA SOLENOIDE

pins = ((VOLUME, 'out')(TEMPERATURA, 'out')(SOL, 'out'), (IRRIGACAO, 'out'), (ILUMINACAO, 'out'),)

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 10000
spi.mode = 0b00
spi.bits_per_word = 8

system_status = 1

dweet = Dweet()

def readDigital(gpio):
	digital = [0,0]
	digital[0] = gpio.digital_read(ILUMINACAO)
	digital[1] = gpio.digital_read(IRRIGACAO)

	return digital

def writeDigital(gpio, digital):
	write = digital
	gpio.digital_write(ILUMINACAO, write[0])
	gpio.digital_write(IRRIGACAO, write[1])

	return digital

def detectaButton(gpio):
	global system_status
	status = gpio.digital_read(BUTTON)
	if status == 1:
		if system_status == 0:
			system_status = 1
			print "Sistema Ligado! \n"
		else:
			system_status = 0
			print "Sistema Desligado \n"

	return system_status


def readVol(gpio):

	gpio.digital_write(VOLUME, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(VOLUME, GPIO.LOW)
	r = spi.xfer2([0x01, (8+3)<<4, 0x00])
	gpio.digital_write(VOLUME, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	#print("Temperatura:%2.1f " %adc_temp)
	return adc_temp

def readTemp(gpio):

	gpio.digital_write(TEMPERATURA, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(TEMPERATURA, GPIO.LOW)
	r = spi.xfer2([0x01, (8+0)<<4, 0x00]) #ADC2
	gpio.digital_write(TEMPERATURA, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)
	adc_temp = (adcout *5.0/1023-0.5)*100

	#print("Temperatura:%2.1f " %adc_temp)
	return adc_temp

def readLumi(gpio):

	gpio.digital_write(ILUMINACAO, GPIO.HIGH)
	time.sleep(0.0002)
	gpio.digital_write(ILUMINACAO, GPIO.LOW)
	r = spi.xfer2([0x01, (8+3)<<4, 0x00])
	gpio.digital_write(ILUMINACAO, GPIO.HIGH)

	adcout = (r[1] << 8) & 0b1100000000
	adcout = adcout | (r[2] & 0xff)

	#print("Luminosidade: %d" %adcout)
	return  adcout

#def readDweet():

if __name__=='__main__':
	with GPIO(pins) as gpio:
		while True:
			digital = [0,0]
			resposta = dweet.latest_dweet(name="murilo_inatel")
			digital[0] =  resposta['with'][0]['content']['iluminacao']
			digital[1] =  resposta['with'][0]['content']['irrigacao']
			writeDigital(gpio, digital)
			temp = readTemp(gpio)
			lumi = readLumi(gpio)
			vol = readVol(gpio)
			digital = readDigital(gpio)
			print "LEITURA: Sistema iRRigacao\n Temperatura: %2.1f\nSol: %d\nIluminacao: %d\nIrrigacao: %d\nVolume Dagua:%d" %(temp,lumi,
			digital[0], digital[1],vol)
			dweet.dweet_by_name(name="murilo_inatel", data={"iluminacao":digital[0],
			"irrigacao": digital[1], "temperatura":temp, "sol": lumi,"volume":vol})

			time.sleep(10)

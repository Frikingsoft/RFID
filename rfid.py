import mfrc522
from os import uname


def do_read():

	if uname()[0] == 'WiPy':
		rdr = mfrc522.MFRC522("GP16", "GP19", "GP18", "GP19")
	elif uname()[0] == 'esp8266':
		rdr = mfrc522.MFRC522(0, 2, 4, 5, 14)
	else:
		raise RuntimeError("Unsupported platform")

	print("---------------------------")
	print(" Inserte Una tarjeta RFID")
	print("---------------------------")

	try:
		while True:

			(stat, tag_type) = rdr.request(rdr.REQIDL)

			if stat == rdr.OK:

				(stat, raw_uid) = rdr.anticoll()

				if stat == rdr.OK:
					print("Se tetecto La tarjeta")
					print(" Tarjeta:	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					print("")

					if rdr.select_tag(raw_uid) == rdr.OK:

						key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

						if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
							
							rdr.stop_crypto1()
						else:
							print("Error de identificacion")
					else:
						print("Failed to select tag")

	except KeyboardInterrupt:
		print("Bye")

do_read()

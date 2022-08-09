import datetime
import time
import socket
from elastic import Elastic
from common import Common

class Adsb:
	def main():

		count_since_commit = 0
		count_total = 0
		failed_attempts = 1
		start_time = datetime.datetime.utcnow()

		# open a socket connection
		while failed_attempts < Common().connect_attempt_limit():
			try:
				Common().log_config()
				s = socket_connection(Common().host(), Common().port())
				failed_attempts = 1
				print("Connected to HertsPi broadcast")
				break
			except socket.error:
				failed_attempts += 1
				print("Cannot connect to HertsPi broadcast. This is retry %s." %
					(failed_attempts))
				time.sleep(Common().connect_attempt_delay())
		else:
			quit()

		data_str = ""
		last_time = start_time

		try:
			# loop until an exception
			while True:
				# get current time
				cur_time = datetime.datetime.utcnow()
				ds = cur_time.isoformat()
				ts = cur_time.strftime("%H:%M:%S")

				# receive a stream message
				try:
					message = ""
					message = s.recv(Common().buffer_size())
					data_str += message.decode().strip("\n")
				except socket.error:
					# Connection to the socket failed, then skip
					pass

				if len(message) == 0:
					print(ts, "No broadcast received. Attempting to reconnect")
					time.sleep(Common().connect_attempt_delay())
					s.close()

					while failed_attempts < Common().connect_attempt_limit():
						try:
							s = socket_connection(Common().host(), Common().port())
							failed_attempts = 1
							print("Reconnected!")
							break
						except socket.error:
							failed_attempts += 1
							print("The attempt failed. Making attempt %s." %
								(failed_attempts))
							time.sleep(Common().connect_attempt_delay())
					else:
						quit()

					continue

				# it is possible that more than one line has been received
				# so split it then loop through the parts and validate

				data = data_str.split("\n")

				for d in data:
					line = d.split(",")

					# if the line has 22 items, it's valid
					if len(line) == 22:

						# add the current time to the row
						line.append(ds)
						if (line[14] == ""):					
							line[14] = 0
							line[15] = 0
						
						if line[21] == ' \r' or line[21] == '\r':					
							line[21] = '1\r'

						#Insert into Elasticsearch
						Elastic().insert(Elastic().format(line))
						
							# increment counts
							
						count_total += 1
						count_since_commit += 1

						# since everything was valid we reset the stream message
						data_str = ""
					else:
						# the stream message is too short, prepend to the next stream message
						data_str = d
						continue

		except KeyboardInterrupt:
			print("\n%s Closing connection" % (ts,))
			s.close()
			print(ts, "%s datapoints added to your database, %s" % (count_total, Common().es_index(),))


	def socket_connection(loc,port):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((loc, port))
		return s

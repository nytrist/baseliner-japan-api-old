from flask_restful import Resource, reqparse, request
from flask_jwt import jwt_required
from models.reading import ReadingModel

import csv
import string
import time


class Reading(Resource):

#get individual reading
	#@jwt_required() - removed authentication
	def get(self, reading_id):
		reading = ReadingModel.find_by_id(reading_id)
		if reading:
			return reading.json()
		return{'message': 'Reading not found'}, 404


class ReadingAdd(Resource):
#add, delete reading
	def post(self):
		#csv in post body of post request
		data = request.data.decode('utf-8')

			#save reading to CSV file
		with open("readings.csv", "a", ) as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow([time.ctime(), data])

		#prep data for db
		lines = data.strip().split('\n')
		for line in lines:
			#print(line)
			data = line.strip().split(',')
			gw_date_time = data[0]

			gw_id = data[1]
			gw_rssi = data[2]
			ss_rssi = data[3]
			gw_conn_att = data[4]
			gw_encl_temp = data[6]
			gw_batt = data[6]
			gw_solar_vol = data[7]

			ss_id = data[8]
			ss_num = data[9]
			ss_conn_att = data[10]
			ss_send_fail = data[11]
			ss_encl_temp = data[12]
			ss_batt = data[13]
			ss_solar_vol = data[14]

			ss_air_temp = data[15]
			ss_baro_press = data[16]
			ss_air_humid = data[17]
			ss_alt = data[18]

			soil_vwcShlw = data[19]
			soil_vwcMid = data[20]
			soil_vwcDeep = data[21]
			soil_ph = data[22]
			soil_temp = data[23]
			soil_co2 = data[24]

			reading = ReadingModel(gw_date_time, gw_id, gw_rssi, ss_rssi, gw_conn_att, gw_encl_temp, gw_batt, gw_solar_vol, ss_id, ss_num, ss_conn_att, ss_send_fail, ss_encl_temp, ss_batt, ss_solar_vol, ss_air_temp, ss_baro_press, ss_air_humid, ss_alt, soil_vwcShlw, soil_vwcMid, soil_vwcDeep, soil_ph, soil_temp, soil_co2)

		try:
			#save to db
			reading.save_to_db()

		except:
			return{"message": "An error occurred inserting the reading."}, 500 # internal server error

		return reading.json(), 201

#delete readings
	def delete(self, reading_id):
		reading = ReadingModel.find_by_id(reading_id)
		if reading:
			reading.delete_from_db()

		return {'message': 'Reading deleted.'}


class ReadingList(Resource):
	def get(self):
		return [reading.json() for reading in ReadingModel.query.all()]

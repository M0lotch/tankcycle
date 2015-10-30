import matplotlib.pyplot as plt
import shelve


tank_list = shelve.open("tanks.txt", flag = "c")
param_list = shelve.open("params.txt", flag = "c")

class Parameters:
	def __init__(self, tank_name, date, ammonia, nitrite, nitrate):
		self.tank_name = tank_name
		self.date = date
		self.ammonia = ammonia
		self.nitrite = nitrite
		self.nitrate = nitrate

	def relay_info(self):
		print("Date: {obj.date}\nAmmonia: {obj.ammonia}\nNitrite: {obj.nitrite}\nNitrate {obj.nitrate}\n".format(obj=self))

class FishTank:
	def __init__(self, name, size, water):
		self.name = name
		self.size = size
		self.water = water
		self.dates_recorded = []

	def relay_info(self):
		print("Name: {obj.name}\nSize(gallons): {obj.size}\nWater: {obj.water}\n-------".format(obj=self))

def add_tank():
	tank_name = input("What is the name of the tank?\n")
	tank_size = input("What size is the tank in gallons?\n")
	tank_water = input("Freshwater, saltwater or brackish?\n")
	tank_name = tank_name.title()
	tank_water = tank_water.title()
	tank_list[tank_name] = FishTank(tank_name, tank_size, tank_water)

def list_tanks():
	print("------")
	for _ in tank_list:
		tank_list[_].relay_info()

def add_parameters(tank):
	date = input("Enter today's date as mm/dd/yy.\n")
	ammonia = input("Enter today's ammonia level.\n")
	nitrite = input("Enter today's nitrite level.\n")
	nitrate = input("Enter today's nitrate level.\n")
	param_list[date] = Parameters(tank, date, ammonia, nitrite, nitrate)
	tank_list[tank].dates_recorded.append(date)

def relay_tank_params(tank):
	try:
		for _ in param_list:
			param_list[_].relay_info()
	except KeyError:
		print("I don't have any recorded parameters for the tank named {}!".format(tank))

def graph_parameters(tank):
	x = []
	y_ammonia = []
	y_nitrite = []
	y_nitrate = []
	try:
		for _ in param_list:
			if param_list[_].tank_name == tank:
				x_point = param_list[_].date
				x_point = x_point.replace("/", "")
				x.append(x_point)
				y_ammonia.append(param_list[_].ammonia)
				y_nitrite.append(param_list[_].nitrite)
				y_nitrate.append(param_list[_].nitrate)
	except KeyError:
		print("I don't have any recorded parameters for the tank named{}.".format(tank))


	plt.plot(x, y_ammonia, label="ammonia")
	plt.plot(x, y_nitrite, label="nitrite")
	plt.plot(x, y_nitrate, label="nitrate")
	plt.xlabel("Dates")
	plt.ylabel("Parameters")
	plt.legend()
	plt.show()


def main():
	running = True
	while running:
		option = input("ADD new tank, USE existing one or QUIT?\n")
		option = option.upper()
		if option == "ADD":
			add_tank()
		elif option == "USE":
			list_tanks()
			tank = input("Which tank would you like to use?\n")
			tank = tank.title()
			if tank in tank_list:
				selection = input("Would you like to ADD new parameters, GRAPH, or VIEW a history of the tank parameters?\n")
				selection = selection.upper()
				if selection == "ADD":
					add_parameters(tank)
				elif selection == "VIEW":
					relay_tank_params(tank)
				elif selection == "GRAPH":
					graph_parameters(tank)

			else:
				print("I don't have records for a tank named{}.".format(tank))				
		elif option == "QUIT":
			tank_list.sync()
			running = False



if __name__ == '__main__':
	main()
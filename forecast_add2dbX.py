from lxml import html
import requests
import sqlite3

page = requests.get('https://magicseaweed.com/Narragansett-Beach-Surf-Report/1103/')
tree = html.fromstring(page.content)


#This will create master list containing SwellSize, SwellInterval, & Airtemp
intervals = tree.xpath('//*[@class="nomargin font-sans-serif heavy"]/text()')
#Navigating through master list, breaking down 3 data categories into variables
swellsizeft = intervals[0::5]
swellintervalsec = intervals[2::5]
airtempdegrees = intervals[4::5]

# Next we will need to iterate through our per category lists, and add to DB!

# ['A', 'B', 'C', 'D']
# ['Swell Size', 'Junk', 'SwellInterval', 'Junk', 'Airtemp']
# ['  2', '  ', '  11', '  ', '38', ]

conn = sqlite3.connect('SurfSend.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS SurfReport(SwellInterval TEXT, AirTemp TEXT )')

for swell in swellintervalsec:

	for airtemp in airtempdegrees:

		conn = sqlite3.connect('SurfSend.db')
		cursor = conn.cursor()
		cursor.execute("INSERT INTO SurfReport VALUES (?,?)", (swell,airtemp))
		conn.commit()
		cursor.close()
		conn.close()



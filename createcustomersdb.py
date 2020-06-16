from application import db, bcrypt
from application.models import Customer
import random as rd

names = ["Liam",
"Noah",
"William",
"James",
"Oliver",
"Benjamin",
"Elijah",
"Lucas",
"Mason",
"Logan",
"Alexander",
"Ethan",
"Jacob",
"Michael",
"Daniel",
"Henry",
"Jackson",
"Sebastian",
"Aiden",
"Matthew",
"Samuel",
"David",
"Joseph",
"Carter",
"Owen",
"Wyatt",
"John",
"Jack",
"Luke",
"Jayden",
"Dylan",
"Grayson",
"Levi",
"Isaac",
"Gabriel",
"Julian",
"Mateo",
"Anthony",
"Jaxon",
"Lincoln"]

addr = ["17 S Chester Rd, Swarthmore, PA, 19081",
"44064 Engle Way #APT 83, Lancaster, CA, 93536",
"Po Box 7570, Urbandale, IA, 50323",
"1502 Murray Ln, Chapel Hill, NC, 27517",
"415 Page Pl, Roswell, GA, 30076",
"229 Secretariat Ct, Ashland, VA, 23005",
"3209 S Michigan St, South Bend, IN, 46614",
"1711 Eagle Watch Dr, Orange Park, FL, 32003",
"9105 79th St S, Cottage Grove, MN, 55016",
"411 Fairway St, Pearisburg, VA, 24134",
]

state=[
"Andra Pradesh",
"Arunachal Pradesh",
"Assam",
"Bihar",
"Chhattisgarh",
"Goa",
"Gujarat",
"Haryana",
"Himachal Pradesh",
"Jammu and Kashmir",
"Jharkhand",
"Karnataka",
"Kerala",
"Madya Pradesh",
"Maharashtra",
"Manipur",
"Meghalaya",
"Mizoram",
"Nagaland",
"Orissa",
"Punjab",
"Rajasthan",
"Sikkim",
"Tamil Nadu",
"Telagana",
"Tripura",
"Uttaranchal",
"Uttar Pradesh",
"West Bengal",
]

city = [
"Hyderabad",
"Itangar",
"Dispur",
"Patna",
"Raipur",
"Panaji",
"Gandhinagar",
"Chandigarh",
"Shimla",
"Srinagar",
"Ranchi",
"Bangalore",
"Thiruvananthapuram",
"Bhopal",
"Mumbai",
"Imphal",
"Shillong",
"Aizawi",
"Kohima",
"Bhubaneshwar",
"Chandigarh",
"Jaipur",
"Gangtok",
"Chennai",
"Hyderabad",
"Agartala",
"Dehradun",
"Lucknow",
"Kolkata",
]

ssnNo = rd.randint(77777777,99999999)
custID = rd.randint(33333333, 99999999)
for i in range(25):
	rdsc = rd.randint(0,28)
	cust = Customer(ssn=ssnNo+1, cust_id=custID+1, cust_name=names[rd.randint(0,39)], cust_address=addr[rd.randint(0, 9)], cust_contact=rd.randint(8888888888,9999999999), cust_age=rd.randint(10,80), cust_state=state[rdsc], cust_city=city[rdsc])
	print(cust)
	ssnNo+=1
	custID+=1
	db.session.add(cust)
	db.session.commit()

customers = Customer.query.all()
for customer in customers:
	print(customer)
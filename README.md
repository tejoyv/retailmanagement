<img src="https://user-images.githubusercontent.com/38109942/85063037-27a5b180-b1c7-11ea-8bbd-807f2238ed13.jpg" align="right"/>

# Retail Management Website [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome#readme)
> Developed Using Flask Web framework

<br>
The System needs to be able to handle primary functions that can be grouped into two set of activities.

New account executive/New customer<br/>
 - Create, Update, Delete Customer<br/>
 - Create and Delete Account<br/>
 - View Customer and Account Status<br/>
 

Cashier/Teller<br/>
- Manage deposit, withdraw and transfer<br/>
- Get Customer and Account details<br/>
- Get Customer-Account Transactions/Get Statement<br/>


### Installing

Clone the repository and activate the virtual environment.
In cmd navigate to the project folder and write: 
```
venv\Scripts\activate
```

Next install the libraries and dependencies :

```
pip install -r requirements.txt
```

Run the website :
```
python main.py
```

### Login Instructions :

- Bank Executive Login -> username = User11111 and password = User@11111
- Cashier Login -> username = User22222 and password = User@22222

### Database used
```
SQLite Database using SQLAlchemy ORM
```

### Project Screenshots :

### 1. Executive Login :

1. Home Page
![Screenshot (269)](https://user-images.githubusercontent.com/38109942/85061457-77cf4480-b1c4-11ea-9ca5-a2935a2eb66e.png)
![Screenshot (270)](https://user-images.githubusercontent.com/38109942/85061507-8ae21480-b1c4-11ea-8738-f23063e804e4.png)
![Screenshot (271)](https://user-images.githubusercontent.com/38109942/85061513-8f0e3200-b1c4-11ea-9eee-d8de3e51b21a.png)
2. Login as Executive
![Screenshot (273)](https://user-images.githubusercontent.com/38109942/85061521-933a4f80-b1c4-11ea-9563-ab3bd2e61a24.png)

3. Customer Creation Form
![Screenshot (275)](https://user-images.githubusercontent.com/38109942/85061719-ea402480-b1c4-11ea-91cd-6ae09cbefa82.png)
4. View All Customer
![Screenshot (276)](https://user-images.githubusercontent.com/38109942/85061558-a3eac580-b1c4-11ea-84c1-7acb8ef67e4b.png)
5. Show Customer Details of an individual customer
![Screenshot (277)](https://user-images.githubusercontent.com/38109942/85061565-a9481000-b1c4-11ea-9206-c1b5d5f7ca84.png)
6. Update Customer details 
![Screenshot (278)](https://user-images.githubusercontent.com/38109942/85061577-aea55a80-b1c4-11ea-9c88-4671341785c8.png)
7. Delete Customer details
![Screenshot (279)](https://user-images.githubusercontent.com/38109942/85061584-b402a500-b1c4-11ea-977a-7b8a00e96a5b.png)
8. Create Account by Executive Form
![Screenshot (280)](https://user-images.githubusercontent.com/38109942/85061592-b8c75900-b1c4-11ea-9852-08974e133a79.png)
9. View all accounts by Executive
![Screenshot (281)](https://user-images.githubusercontent.com/38109942/85061605-bfee6700-b1c4-11ea-8e57-8cb3f6d621d6.png)
10. Search Account by Executive
![Screenshot (282)](https://user-images.githubusercontent.com/38109942/85061618-c5e44800-b1c4-11ea-8b96-fb004bb74511.png)

### 2. Cashier Login :
1. Login as Casier
![Screenshot (283)](https://user-images.githubusercontent.com/38109942/85061991-5f135e80-b1c5-11ea-8514-bc87489de14c.png)
2. Dashboard for Cashier
![Screenshot (284)](https://user-images.githubusercontent.com/38109942/85061999-63d81280-b1c5-11ea-8490-7210c3259ccc.png)
3. Search Account 
![Screenshot (286)](https://user-images.githubusercontent.com/38109942/85062016-689cc680-b1c5-11ea-96a0-5a7263a295d4.png)
![Screenshot (287)](https://user-images.githubusercontent.com/38109942/85062026-6c304d80-b1c5-11ea-8fa6-b56485d60cab.png)
4. Withdraw Money by cashier
![Screenshot (288)](https://user-images.githubusercontent.com/38109942/85062045-705c6b00-b1c5-11ea-88c4-d74fc6cdc848.png)
5. Deposit Money by cashier
![Screenshot (290)](https://user-images.githubusercontent.com/38109942/85062072-78b4a600-b1c5-11ea-8a41-2285fd95ad80.png)
![Screenshot (291)](https://user-images.githubusercontent.com/38109942/85062080-7d795a00-b1c5-11ea-974d-1f797c38d72b.png)
6. Transfer Money by cashier
![Screenshot (292)](https://user-images.githubusercontent.com/38109942/85062089-810ce100-b1c5-11ea-89e9-3c36eb74b6e7.png)
7. Detailed Statement
![Screenshot (293)](https://user-images.githubusercontent.com/38109942/85062096-84a06800-b1c5-11ea-89bc-34ea0b8af935.png)

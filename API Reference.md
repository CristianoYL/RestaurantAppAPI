# API Reference
Below is the reference of all the available APIs of this project, which might be helpful for future reference.

## User
## POST ```/auth```
User authentication using flask-jwt.
##### params:
```
username: (string, required) the phone number of the user

password: (string, required) the password of the user
```

## GET ```/user```
Get all users' id and phone number
#### POST ```/user```
Register a new user if not exists
##### params:
```
phone: (string, required) the phone number of the user

password: (string, required) the password of the user
```
## PUT ```/user/password```
Use JWT to identify current user and change this user's password
##### params:
```
password: (string, required) the new password
```
## GET ```/user/id/<<int:userID>>```
Get the user with specified user ID
## DELETE ```/user/id/<<int:userID>>```
Delete the user with the specified user ID

## /restaurant
### Allowed Methods
#### GET:
Get all restaurants' info
#### POST:
Create a new restaurant with given params
##### params:
name: (string, required) name of the restaurant

fee: (float, required) the service fee of the takeout

limit: (float, required) the least price of the takeout

address: (string, required) the full physical address of the restaurant

openTime: (string, required) the open time (for takeout) of the restaurant

closeTime:(string, required) the close time (for takeout) of the restaurant

isOpen: (boolean, optional, default = true) whether the restaurant is open for business

logo: (string, optional) the url of the restaurant's logo image

promo: (string, optional) the promotion info of the restaurant

phone: (string, required) the contact phone number of the restaurant


## /menu
### Allowed Methods
#### GET:
Get all restaurants' menu info
#### POST:
Create a new menu item for specified resaurant with given params
##### params:
rid: (int, required) ID of the restaurant to add menu

name: (string, required) name of the food

price: (float, required) the price of the food

category: (string, required) the category of the food

description: (string, optional) the description of the food

spicy: (int, optional, default = 0) the spicy level of the food, 0 = not spicy etc.

isAvailable: (boolean, optional, default = true) whether the food is available now

isRecommended: (boolean, optional, default = false) whether the food is the restaurant's recommendation

## menu/id/<<int:id>>
### Allowed Methods
#### GET:
Get the menu item with specified menu ID
#### PUT:
Update the menu item for specified menu ID with given params
##### params:
name: (string, optional) name of the food

price: (float, optional) the price of the food

category: (string, optional) the category of the food

description: (string, optional) the description of the food

spicy: (int, optional) the spicy level of the food, 0 = not spicy etc.

isAvailable: (boolean, optional) whether the food is available now

isRecommended: (boolean, optional) whether the food is the restaurant's recommendation




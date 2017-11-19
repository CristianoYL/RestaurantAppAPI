# API Reference
(Updated on 11/15/2017)

Below is the reference of all the available APIs of this project, which might be helpful for future reference.

Before diving into details, here's some tips about the APIs.

* When an endpoint requires ```JWT``` authentication, please include the ```Authorization``` Header and ```JWT``` like this:
```
{"Authorization" : "JWT <the according access token>"}
```
Beware that there is a space between JWT and the access token, unfortunately.

In this reference, we will denote the endpoint as **jwt_required** if ```JWT``` token is required to access the endpoint, and we denote admin identity requirement by **admin_jwt_required**
* When the queried endpoint returns an error, ```500```, ```404```, ```401```, ```400``` etc. You may use the key ```message``` to retrieve the error info.
# Endpoints
## User
#### POST ```/auth```
User authentication using flask-jwt. Returning a JWT if authenticated, else return ```401 UNAUTHORIZED```
##### params:
```
{
  "username": <(string, required) the phone number of the user>
  "password": <(string, required) the password of the user>
}
```

#### GET ```/user```
**admin_jwt_required** Get all users' id, stripeID, email and phone number. If authorized, return list of ```User```s
```
{
  "users":[{
                'id' : user.id,
                'stripeID' : user.stripeID,
                'email' : user.email,
                'phone':user.phone
            },
            ...
            ]
}
```
#### POST ```/user```
Register a new user if not exists, and return the created `User` with status code```201 CREATED```. Else return ```400``` if already exists or ```500``` if there's an error.
##### params:
```
{
  "phone": <(string, required) the phone number of the user>
  "password": <(string, required) the password of the user>
}
```
#### PUT ```/user/password```
**jwt_required** Use JWT to identify current user and change this user's password.
##### params:
```
{
  "password": <(string, required) the new password>
}
```
#### GET ```/user/id/<int:userID>```
**admin_jwt_required** Get the user with specified user ID. If authorized, return the found ```User```
```
{
  "user" : {
              'id' : user.id,
              'stripeID' : user.stripeID,
              'email' : user.email,
              'phone':user.phone
              'password' : user.password
            }
}
```
If not found, return ```404```
#### DELETE ```/user/id/<int:userID>```
**admin_jwt_required** Delete the user with the specified user ID

## Restaurant
#### GET ```/restaurant```
Get all restaurants' info. Return list of all ```Restaurant```s
```
{
  "restaurants":[<list of restaurants>]
}
```
#### POST ```/restaurant```
Create a new restaurant with given params
##### params:
```
{
  "name": <(string, required) name of the restaurant>
  "fee": <(float, required) the service fee of the takeout>
  "limit": <(float, required) the least price of the takeout>
  "address": <(string, required) the full physical address of the restaurant>
  "openTime": <(string, required) the open time (for takeout) of the restaurant>
  "closeTime": <(string, required) the close time (for takeout) of the restaurant>
  "isOpen": <(boolean, optional, default = true) whether the restaurant is open for business>
  "logo": <(string, optional) the url of the restaurant's logo image>
  "promo": <(string, optional) the promotion info of the restaurant>
  "phone": <(string, required) the contact phone number of the restaurant>
}
```

#### PUT ```/restaurant/id/<int:id>```
**admin_jwt_required** Update an existing restaurant with given params
##### params:
```
{
  "name": <(string, optional) name of the restaurant>
  "fee": <(float, optional) the service fee of the takeout>
  "limit": <(float, optional) the least price of the takeout>
  "address": <(string, optional) the full physical address of the restaurant>
  "openTime": <(string, optional) the open time (for takeout) of the restaurant>
  "closeTime": <(string, optional) the close time (for takeout) of the restaurant>
  "isOpen": <(boolean, optional, default = true) whether the restaurant is open for business>
  "logo": <(string, optional) the url of the restaurant's logo image>
  "promo": <(string, optional) the promotion info of the restaurant>
  "phone": <(string, optional) the contact phone number of the restaurant>
}
```
If Authorized, return the updated ```Restaurant``` object, else return ```401```, ```404``` or ```500``` accordingly.

## Menu
#### GET ```/menu```
**admin_jwt_requried** Get all restaurants' menu info. Return list of all menus:
```
{
  "menus":[<list of menu>]
}
```

#### POST ```/menu```
**admin_jwt_requried** Create a new menu item for specified resaurant with given params
##### params:
```
{
  "rid": <(int, required) ID of the restaurant to add menu>
  "name": <(string, required) name of the food>
  "price": <(float, required) the price of the food>
  "category": <(string, required) the category of the food>
  "description": <(string, optional) the description of the food>
  "spicy": <(int, optional, default = 0) the spicy level of the food, 0 = not spicy etc.>
  "isAvailable": <(boolean, optional, default = true) whether the food is available now>
  "isRecommended": <(boolean, optional, default = false) whether the food is the restaurant's recommendation>
}
```
Return ```200``` and the created ```Menu``` object if succeeded, else return ```400``` or ```500``` accordingly.
#### GET ```menu/id/<int:id>```
Get the menu item with specified menu ID. If found, return ```200``` and the ```Menu``` object, else return ```404```.

#### PUT ```menu/id/<int:id>```
**admin_jwt_required** Update the menu item for specified menu ID with given params
##### params:
```
{
  "name": <(string, required) name of the food>
  "price": <(float, required) the price of the food>
  "category": <(string, required) the category of the food>
  "description": <(string, optional) the description of the food>
  "spicy": <(int, optional, default = 0) the spicy level of the food, 0 = not spicy etc.>
  "isAvailable": <(boolean, optional, default = true) whether the food is available now>
  "isRecommended": <(boolean, optional, default = false) whether the food is the restaurant's recommendation>
}
```
Return the updated ```Menu``` object with ```200``` if authorized and succeeded. Else return ```401```, ```404```, ```500``` etc. accordingly.

#### GET ```/menu/restaurant/id/<int:rid>```
Get the specified restaurant's menus by restaurant's id. Return list of ```Menu```s if the restaurant exists.
```
{
  "menus":[<list of menu>]
}
```
Return ```404``` if restaurant not found.

## Transaction
#### POST ```/transaction/ephemeral_key```
**jwt_required** Get a Ephemeral Key for the current user for his future transaction with Stripe.
##### params
```
{
  "stripe_api_version" : "<(String, required) the current in-use API version of Stripe>"
}
```
Returns the ```ephemeral key``` if succeeded:
```
{
    "ephemeral_key": <ephemeral key>
}
```
Else return ```404``` or ```500``` accordingly.

## Order
Still under development...

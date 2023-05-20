# EcommerceApp

This is the Ecommrece App written in Django with function based views using django-signals and PayPal payment option.
This app is made to create an ecommerce platform where user can stock items in cart and then finalize it with PayPal payment option.
Buying is possible for logged in and not logged in users. Application was tested with PayPal Sandbox platform.

## App supports:
- User registration with **django-signals** which are used for creating and connecting User model with OneToOneLinked Customer profile
- Logging
- Possibility of stocking items with cart based on cookies
- Finalize the order with **PayPal** payment option.
- Possibility of making shopping as Anonymous user also as logged in user
- Updating amount of items in cart with on cart view based on **JS fetch**
- Ranking products
- Commenting products
- Pagination of comments
- Pagination of products
- Searching through products with category based filter


## Screenshoots from app:

### Main page of the app
![main page of the app](https://github.com/sDebski/studbuddy/blob/master/images/store.png?raw=true)
---

### Profile
![profile](https://github.com/sDebski/studbuddy/blob/master/static/images/profile.png?raw=true)
---

### Recent activites
![Recent activites](https://github.com/sDebski/studbuddy/blob/master/static/images/recent-activites.png?raw=true)
---

### Room
![Room](https://github.com/sDebski/studbuddy/blob/master/static/images/room.png?raw=true)
---


### Room creation
![Room-creation](https://github.com/sDebski/studbuddy/blob/master/static/images/room-create.png?raw=true)
---

### Browse topics
![Browse-topics](https://github.com/sDebski/studbuddy/blob/master/static/images/browse-topics.png?raw=true)
---

The app is based on tutorial [Django App](https://www.youtube.com/watch?v=PtQiiknWUcI).



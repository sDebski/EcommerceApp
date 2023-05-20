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
![main page of the app](https://github.com/sDebski/EcommerceApp/blob/master/images/store.png?raw=true)
---

### Cart view
![Cart-view](https://github.com/sDebski/EcommerceApp/blob/master/images/cart-view.png?raw=true)
---

### Payment View
![Payment-view](https://github.com/sDebski/EcommerceApp/blob/master/images/payment-view.png?raw=true)
---

### PayPal payment
![PayPal-payment](https://github.com/sDebski/EcommerceApp/blob/master/images/payment.png?raw=true)
---

### Anonymous buy
![Anonymous-buy](https://github.com/sDebski/EcommerceApp/blob/master/images/anonymous-buy.png?raw=true)
---

### View item
![View-item](https://github.com/sDebski/EcommerceApp/blob/master/images/view-item.png?raw=true)
---

### Browse products
![Browse-products](https://github.com/sDebski/EcommerceApp/blob/master/images/categories.png?raw=true)
---

### Registration
![Registration](https://github.com/sDebski/EcommerceApp/blob/master/images/registration.png?raw=true)
---





The app is based on tutorial [Django App](https://www.youtube.com/playlist?list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng).



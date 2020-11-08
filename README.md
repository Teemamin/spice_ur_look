# SpiceUrLook Project
----
SpiceUrLook project is a fictitious online store that provides a unique customer experience: This includes giving a
 personalized experience to each customer or visitor of the website, options of responsive view point from devices of 
 varying screen size and easy login via google social login.

 ## UX 
 ----
 ### Main Aims:
 * Promoting and selling  products online.
 * Establishing brand awareness and corporate identity.
 * Generating revenue and providing a unique customer experience
 * Boosting the efficiency of services
 * Developing relevant target

 ### User Stories :
 ----

 The following User Stories helped me to create a design that would satisfy the needs of several different types of users:
 
 #### Project stakeholder / Product Owner:
 * As the major stakeholder / product owner my main aim is  to generate revenue – to be very efficient at selling
  through understanding complex consumer behaviour to maximise conversion rates
  and up-sell and cross-sell products and services to maximise value over the lifetime of the customer.

#### Site Users:
| As A User  | Actions to  perform                                                                    | Goals to achieve                                                                                                                                      |
|------------|----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| user       | easily register for an account, have option of using a social account to register      | To have a personalized account to be able to view my profile, rate products and add products to wish-list                                             |
| user       | easy login / logout with social account options                                        | to access my account information                                                                                                                      |
| user       | easy password recovery, incase I cannot remember                                       | regain access to my account                                                                                                                           |
| user       | have a personalized user profile                                                       | to save my default payment/delivery details, view past order history and confirmations                                                                |
| user       | receive email confirmation upon sign up or password rest                               |                                                                                                                                                       |
| user       | View products by gender, category or price                                             | Make a selection to buy or add to wish-list                                                                                                           |
| user       | view individual product details                                                        | identify product price, ratings, full size image, description, size, color and option to rate the product if the user has previously bought the item  |
| user       | search products                                                                        | to buy or add to wish-list for later purchase                                                                                                         |
| user       | easily see the result of my search and the number of products available for the search | quickly identify if the product I am searching for is available                                                                                       |
| user       | easy access to products on sales and promotions                                        | take advantage of budget buying / shopping                                                                                                            |
| user       | easily access the total of bag items at all time to avoid going over budget            | to avoid spending too much                                                                                                                            |
| user       | sort products by either price or category                                              | to easily find products based on the best prices and category of interest                                                                             |
| user       | easily add, subtract or delete products from my shopping bag                           | ensure I can easily keep to my budget                                                                                                                 |
| user       | easily view all selected products in my shopping bag to be bought                      | see the total cost and quantity                                                                                                                       |
| user       | easily enter my card payment details to at checkout                                    | checkout easy                                                                                                                                         |
| user       | have peace of mind that the payment process and my card details are secure             | confidently provide the necessary info to complete the payment                                                                                        |
| user       | easily view my order details after checkout is successful                              | to have a verified copy of my purchase                                                                                                                |
| user       | receive a confirmation email with the details of my purchase                           | to have a copy of my confirmation                                                                                                                     |
| site-owner | add products                                                                           | add products to be sold on my site                                                                                                                    |
| site-owner | edit / update product                                                                  | to easily make changes to any product attribute eg price, name or description                                                                         |
| site-owner | delete product                                                                         | to easily remove product from the site.                                                                                                               |

#### Wireframes: 
* Click to view [wireframes](https://github.com/Teemamin/spice_ur_look/blob/master/wireframes/spiceurlook_wireframes.pdf).
#### Databse Design: 
* Click to view [database diagram](https://github.com/Teemamin/spice_ur_look/blob/master/databse_design/SpiceurlookModels.pdf).


### Features
----
#### Existing Features:
This  Django project consists of five applications and eight modules.
1. Accounts/Registration:

* Registration: a user can register for an account, upon successfull registration a confirmation email is sent to the 
user's provided email address
* Google social login: a user has the option to login to our site with their google account 
* Login / logout: a user can easily login with their registered details
* Password reset: a user can easily recover their password incase they forget it.
* Note: if running this project on gitpod: for social login to work: run python3 manage.py runserver 0.0.0.0:8000

2. Site Navigation: is consistent accross the site it allows the user to do the following:

* Browse the site by gender and category
* Browse the site by price 
* Browse the site by sales and promotions
* Search fucntionality via the search icon
* User login, logout, sign-in, sign-out and social login option
* Access to user profile (available to authenticated users)
* Access to wishlist (available to authenticated users)
* Access to shopping bag via the bag icon

3. Products App:

* product sorting :a user can sort the products by:
- price ascending
- price descending
- sales ascending
- sales descending
* Wishlist : authenticated users have the option to add/remove any product to their wishlist, for a later purchase
wishlist items are available for the user to revisit at a anytime if they are logged in
* Product rating : rating option is available for authenitacted users who have bought the product
* Size selection : if product has a size : users have the option to chose  product size to purchase
* Quantity : users get to chose from 1 to 50 qty of a particular product to add to shopping bag
* site owner:
- can add a product
- edit / update a product 
- delete a product 

4. Profiles App: 

* Personalized profile page: a registered user can fill-up a default delivery/shipping details on their profile page
which will be used during their checkout to make it process faster and more convenient.
- a user can add, update and delete their personal info
* Past order summary: a users profile page automatically save all their past order summary and confirmations

5. Shopping_bag :

* Displays selected products to be purchased and its details 
* Users can add and reduce product quantity from the shpping bag and the cost will adjust accordingly 
* Users can remove selected products from the shipping bag and cost will adjust accordingly
* Proceed to checkout page

6. Checkout App:

* If a user is authenticated and has a profile the delivery/shipping form will be pre-populated with their default 
info else if the user is not authenticated the form will be empty 
* A summary of the products & cost the user is about to purchase will be avaible on display next to the delivery/shipping form
* Stripe secure card validation: the card entered by the user will be validated in real time by stripe and if valid:
the purchase will go through and the user will be automatically redirected to success page showing order confirmation details
* Upon successful purchase: confirmation email is sent to the user, containing their order summary

#### Features Left to Implement:

* A future feature could be adding set of filters that will allow the site user to browse the site by things like:
- size, color or brand
* online customer service chat platform 
* An overlay of a quick shopping
* Additional payment methods like paypal or applepay

### Technologies Used

Languages, libraries, frameworks, editors and version control:

* HTML5 was used to put the page structure in place [HTML5](https://validator.w3.org/).
* CSS was used to style and allign images and other structures on the page [CSS](https://www.w3.org/Style/CSS/Overview.en.html).
* Javascript was used for interactivity [JavaScript](https://www.ecma-international.org/).
* Python3 was used for the application scripting [Python](https://www.python.org/).
* Django framework was used to build the Project [Django](https://www.djangoproject.com/).
* Heroku for hosting the application [Heroku](https://dashboard.heroku.com/apps).
* Amazon web service was used to host static and media files [AWS](https://aws.amazon.com/).
* Postgres database was used for the deployed app on heroku [Postgres](https://www.postgresql.org/).
* Gunicorn server was used for the deployed app on heroku [Gunicorn](https://gunicorn.org/).
* Stripe payment service was used for product payments [Stripe](https://stripe.com/).
* Bootstrap was used for page layout [Bootstrap](https://getbootstrap.com/).
* Google fonts was used for the site fonts [Google fonts](https://fonts.google.com/).
* Fontawesome was used for its icons [Font awesome](https://fontawesome.com/).
* I used gitpod's development environment to write the code for this project [Gitpod](https://www.gitpod.io/).
* I used github for its repo and version control of the project [Github](https://github.com/).
* I used google smtp email to send emails to users [google](https://support.google.com/mail/answer/7126229?hl=en).


### Testing
----
* Click to view the test file [test file](https://github.com/Teemamin/spice_ur_look/blob/master/test.md).

### Deployment
----
* Click to view the project deployment process [deployment file](https://github.com/Teemamin/spice_ur_look/blob/master/project_deployment.md).

#### Credits

* Code Institute.
* Css Tricks


#### Content

* The content of this website is mostly fictitious and written by myself.

#### Media

* Some of the photos used in this site were obtained from :
1. [Unsplash freestocks](https://unsplash.com/).
2. [Pixels](https://www.pexels.com/).
3. [google](https://www.google.com/).
4. [kaggle paramaggarwal](https://www.kaggle.com/paramaggarwal/fashion-product-images-dataset).


#### Acknowledgements













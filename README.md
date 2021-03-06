# jogging_track

## Write an application that tracks jogging times of users

User must be able to create an account and log in. (If a mobile application, this means that more users can use the app from the same phone).

When logged in, a user can see, edit and delete his times he entered.

Implement at least three roles with different permission levels: a regular user would only be able to CRUD on their owned records, a user manager would be able to CRUD users, and an admin would be able to CRUD all records and users.

Each time entry when entered has a date, distance, and time.

When displayed, each time entry has average speed.

Filter by dates from-to.

Report on average speed & distance per week.

REST API. Make it possible to perform all user actions via the API, including authentication (If a mobile application and you don’t know how to create your own backend, you can use Firebase.com or similar services to create the API).

In any case, you should be able to explain how a REST API works and demonstrate that by creating functional tests that use the REST Layer directly. Please be prepared to use REST clients like Postman, cURL, etc. for this purpose.

If it’s a web application, it must be a single-page application. All actions need to be done client side using AJAX, refreshing the page is not acceptable. (If a mobile application, disregard this).

Minimal UI/UX design is needed. You will not be marked on graphic design. However, do try to keep it as tidy as possible.

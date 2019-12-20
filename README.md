# unit3-build-dummy-api
A dummy API for the Unit 3 Build.

Endpoints:
/reset: drops and recreates the database.
/dbload: loads entries from the .csv file into the database.
/feed: returns all entries from the database in JSON format.
/user/<username>: returns a user's average comment toxicity, total comment toxicity, and their top ten most toxic comments.

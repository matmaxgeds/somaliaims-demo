#  somaliaims project
-------------

## Developer guidelines

The development process of this project follows the gitflow concept

* master - production
* develop - staging
* feature branches - this will be for any feature you are working
* releases

## Notes

* Feature branches automatically branch out of the main develop branch
* Commiting to develop branch directly or the master branch shall not be acceptable
* All work shall be done on it own branch and after done a pull request to be submitted for review.
* You cannot merge your branch to develop, the other developer or technical lead are the only who can merge.


## Requirements

* Python 3.4
* Django 1.8
* Postgres 9

## Setup

* Install Python 3.4
* Set up virtual environment
  ```
   ./manage.py migrate
  ```
  
  ```
   ./manage.py runserver
   ```





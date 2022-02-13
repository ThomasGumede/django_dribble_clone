# Dribble Clone

## Description

Dribble clone developed using django, tailwindcss and jquery/javascript.

## Features

- Add/View/Delete Shots
- Like/Dislike Shots
- Follow/Unfollow dribble clone users
- Add/Remove/View shot feedback
- create/delete collection(TODO)
- Add/Remove shots from collection(TODO)

# Documentation

## Run project

- python -m venv env
- activate environment
- pip install -r requirements.txt
- python manage.py makemigrations {app_name} "start migrating accounts app first"
- python manage.py migrate {app_name}
- python manage.py migrate
- python manage.py runserver

## Shot Add/View/Delete(TODO)
- /
![ ](docs/shots/img.png)

- uploads/new
![ ](docs/shots/img2.png)

- shot/{shot_uuid}
![ ](docs/shots/img3.png)

![ ](docs/shots/img4.png)

## Account Register/Login/Reset password

- account/login
![ ](docs/account/im.png)

- account/signup
![ ](docs/account/im2.png)

- account/password/reset_password
![ ](docs/account/im3.png)

- account/password/token/token
![ ](docs/account/im5.png)



## Account View/Update/Change password/Delete(TODO)

- account/username/id
![ ](docs/account/1mg1.png)

- account/general/username/id
![ ](docs/account/img1.png)

- account/update/username/id
![ ](docs/account/img2.png)

- account/password
![ ](docs/account/img3.png)

## Like/Dislike Shot

- No styled UI

## Follow/Unfollow Users

- No styled UI
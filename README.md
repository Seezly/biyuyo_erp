# BIYUYO ERP

Biyuyo is a full open-source ERP ecosystem made with love by a Venezuelan for Venezuelans.

## Why?

Biyuyo was made with small and informal businesses in mind. Taking into account that [informal labor is almost 70%](https://poli-data.com/informe-sobre-la-informalidad-laboral-en-venezuela-y-su-contexto-regional-2024-2025/#:~:text=Seg%C3%BAn%20estimaciones%20de%20la%20consultora,laboral%20en%20un%20alarmante%2084.5%25.), I thought it would be a **great** idea to make a solution for those small businesses that want and **need** a full ERP for their business and personal finances, but without the hustle and complications attached to a conventional ERP.

That's where Biyuyo enters the room to change the perspective of financial business management.

## Tech Stack

Biyuyo is made based in a rock-solid tech stack, aligned with my desire to explore other technologies:

### Front-end

- Vue.js

- Vite

- TailwindCSS

### Back-end

- Python (with Django)

- Django Rest Framework

- Django Rest Framework Simple JWT

### Database

- PostgreSQL

### Infrastructure

- Docker

## How can I install this project?

### Clone this repo

First things first: you have to clone this repo using the terminal and running the following commands:

`git clone https://github.com/Seezly/biyuyo_erp.git`

### Install dependencies and set-up environment variables

Now that you have cloned this repo, you have to install both front-end and back-end dependencies:

#### Backend

##### Enter the backend directory:

`cd backend`

##### Start the virtual environment with:

`python -m venv venv`

##### Install all the required dependencies:

`pip install -r requirements.txt`

##### Now that both frontend and backend are ready, we now have to copy or .env.example file into .env, so we can declare our environment variables:

`cp .env.example .env`

**Done! You have your backend ready to go.**

#### Frontend:

##### Enter the frontend directory:

`cd frontend`

##### Install all the required dependencies:

`npm install`

##### Build the frontend

`npm run build`

**Done! You have your frontend ready to show.**

### Database

We're almost there! Now, we are going to make migrations. But first, please be sure your PostgreSQL server is up and all the credentials are correct **and** are inside the environment variables in .env

Of course, you will have to create a new database with the information you've written in the environment variables before going any further.

#### Make migrations:

`python manage.py migrate`

### Before start

Before starting the project, please create a superuser and verify all is in order to continue!

### Create superuser:

`python manage.py createsuperuser`

#### Start the backend!:

`python manage.py runserver`

**We're ready to go.**

### Installation using Docker:

You will have to follow the above steps for copying and edit the .env file both in backend directory and root directory. Then you're free to execute the following command (make sure you have Docker Compose installed and running):

For development:
`docker compose -f docker-compose.dev.yml up --build`

For production:

`cd backend`

`cp .env.example .env.production` (Don't forget to change the variables)

`docker compose -f docker-compose.prod.yml up --build`

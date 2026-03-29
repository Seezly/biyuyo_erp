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

1. First things first: you have to clone this repo using the terminal and running the following commands:

`git clone https://github.com/Seezly/biyuyo_erp.git`

2.  Now that you have cloned this repo, you have to install both front-end and back-end dependencies:

    2.1. Backend:

        2.1.1. Enter the backend directory:

        `cd backend`

        2.1.2. Start the virtual environment with:

        `python -m venv venv`

        2.1.3. Install all the required dependencies:

        `pip install -r requirements.txt`

        Done! You have your backend ready to go.

    2.2. Frontend:

        2.2.1. Enter the frontend directory:

        `cd frontend`

        2.2.2. Install all the required dependencies:

        `npm install`

        2.2.3. Build the frontend

        `npm run build`

        Done! You have your frontend ready to show.

3.  Now that both frontend and backend are ready, we now have to copy or .env.example file into .env, so we can declare our environment variables:

`cd backend`

`cp .env.example .env`

4. We're almost there! Now, we are going to make migrations. But first, please be sure your PostgreSQL server is up and all the credentials are correct **and** are inside the environment variables in .env

    4.0. Of course, you will have to create a new database with the information you've written in the environment variables before going any further.

    4.1. Start the backend!:

    `python manage.py runserver`

    4.2. Make migrations:

    `python -m django-admin migrate`

    We're ready to go.

5. Installation using Docker:

`docker compose --env-file ./backend/.env up --build`

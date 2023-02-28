## Introduction
The boundaries of knowledge is constantly expanding in different fields. Achieving quality education in every field is not possible. Sometimes we fail to come across such teachers who can provide us with sufficient guidance. So we identified this serious issue and also tried to solve it through AI for a skilfully educated future. 

### Our motivation : 
Drawbacks faced in online education due to insufficient study     materials, miscommunication and failure in mutual time management degraded its quality. Meanwhile AI reached its heights with technological developments with socio-economic benefits. Hence we merged these two scenarios and found a pioneering system to incorporate AI to impart knowledge to students in the simplest and most efficient ways.

### Impact 
Since AI can connect to users audio-visually at any time through our web app, students can get answers to their query at any time within a short span. Due to no limitation of database and capability of generating images of desired topics, the application wont have any check to the subjects to explore.
## Features

This is a educational application which helps personal development of students from any age group and in any educational field.

- Personalized learning
- Intelligent tutoring systems
- Student data analysis
- An AI powered chatbot where student can ask for any question
- An AI powered system which generated courses as per searched keyword
- User Profile section where student can also keep track of his/her personal growth
- Authentication which includes user-regisration, login, email-verification, reset-password, otp-generation
## Tech Stack

**Client Side:** HTML, CSS, SCSS, TailwindCSS, JavaScript

**Server Side:** Python, Django, Redis

**Database:** SQLite
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`DEBUG = TRUE`

`SECRET_KEY = 'django-insecure-lcu2s1v)m50-l#$mpapl3cx!=jwj=(i9=^67-)kipy1^-d!2sn`

`OPENAI_API_KEY = Your API key`

For the OPENAI_API_KEY go to OpenAi's webiste : https://openai.com/api/ from there signup (or login if you have account). Then generate an API key and put it in the .env file

### For sending emails
`EMAIL_HOST_USER = 'email address from which email will be send'`

`EMAIL_HOST_PASSWORD = 'its app password' `

Note : You have to create app password for the email you are using in `EMAIL_HOST_USER` and put it in `EMAIL_HOST_PASSWORD`

## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/Think-in-Sphere

```
or simply download this project fromhttps://github.com/Mr-Atanu-Roy/Think-in-Sphere

In project directory Create a virtual environment of any name(say env)

```bash
  virtualenv env

```
Activate the virtual environment

For windows:
```bash
  env\Script\activate

```
Install dependencies
```bash
  pip install -r requirements.txt

```
To migrate the database run migrations commands
```bash
  py manage.py makemigrations
  py manage.py migrate

```

Create a super user
```bash
  py manage.py createsuperuser

```
Then add some data into database


To run the project in your localserver
```bash
  py manage.py runserver

```
## Authors

- [@Atanu Roy](https://github.com/Mr-Atanu-Roy)
- [@Rickey](https://github.com/Ricky2054)
- [@Sagarika](https://github.com/Sagarika-02)
- [@Sayanika](https://github.com/Sagarika-02)


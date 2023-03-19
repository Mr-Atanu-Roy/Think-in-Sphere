## Introduction
The boundaries of knowledge is constantly expanding in different fields. Achieving quality education in every field is not possible. Sometimes we fail to come across such teachers who can provide us with sufficient guidance. So we identified this serious issue and also tried to solve it through AI for a skilfully educated future. 

## Features

This is a educational application which helps personal development of students from any age group and in any educational field.

- Personalized learning
- Intelligent tutoring systems
- Student data analysis
- An AI powered chatbot where student can ask for any question
- An AI powered system which generate topics related to searched courses and also generate summery, notes, important questions related to those topics.
- Exam system for each individual topics of a course
- User Profile section where student can also keep track of his/her personal growth
- Authentication which includes user-regisration, login, email-verification, reset-password, otp-generation, google-recaptcha.
## Tech Stack

**Client Side:** HTML, CSS, SCSS, TailwindCSS, JavaScript

**Server Side:** Python, Django, Redis

**Database:** SQLite

**Integrations:** Google Charts, Gmail, Google Translate, Google Speech Recognition, Google Text to Speech, Google reCAPTCHA, Google Authentication, Google Fonts, OPENAI

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

- Django settings

`DEBUG = TRUE`

`SECRET_KEY = 'django-insecure-lcu2s1v)m50-l#$mpapl3cx!=jwj=(i9=^67-)kipy1^-d!2sn`

- OPENAI API

`OPENAI_API_KEY = Your API key`

For the `OPENAI_API_KEY` go to OpenAi's webiste : https://openai.com/api/ from there signup (or login if you have account). Then generate an API key and put it in the .env file

- For sending emails
`EMAIL_HOST_USER = "email address from which email will be send"`

`EMAIL_HOST_PASSWORD = "its app password"`

Note : You have to create app password for the email you are using in `EMAIL_HOST_USER` and put it in `EMAIL_HOST_PASSWORD`

- For Google reCAPTCHA

`RECAPTCHA_PUBLIC_KEY = "your site key"`

`RECAPTCHA_PRIVATE_KEY = "your secret key"`

For `RECAPTCHA_PUBLIC_KEY` and `RECAPTCHA_PRIVATE_KEY` go to https://www.google.com/recaptcha/admin/ from there signup (or login if you have account). Then generate an the API keys and put it in the .env file
## Installation

Create a folder and open terminal and install this project by
command 
```bash
git clone https://github.com/Mr-Atanu-Roy/Think-in-Sphere

```
or simply download this project from https://github.com/Mr-Atanu-Roy/Think-in-Sphere

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

## Detailed Architecture

### Entity Relationship Model -
- ER Model -

![ER Diagram](https://user-images.githubusercontent.com/100309120/226158517-8e17b002-d054-42c6-99e6-6a660bc56479.png)

### Data Flow Diagram -
- DFD -

![DFD](https://user-images.githubusercontent.com/100309120/226158538-b2a40cde-689c-48e7-97b1-4047a06c486c.png)

### High Level Components -
- Authentication System -

**Signin/Registration:** Responsible for registering a user in our application

![SignIn DFD (1)](https://user-images.githubusercontent.com/100309120/226158544-29f790b7-f329-49d1-a0c4-a964f98c3e00.png)

**Login:** Responsible for loging in a user

![Login DFD (1)](https://user-images.githubusercontent.com/100309120/226158550-f9ab6e1d-7e16-4b16-863f-f17fb831f623.png)

- Chatbot -

![ChatBot DFD](https://user-images.githubusercontent.com/100309120/226158555-f928c17a-9f33-445c-a4df-ba6c427ce5f6.png)

- Courses -

![Course DFD](https://user-images.githubusercontent.com/100309120/226158564-f8ec497e-2f37-49cd-b1de-ff4b54bfae5d.png)

- Dashboard-

![Dashboard DFD](https://user-images.githubusercontent.com/100309120/226158600-251be959-4390-4321-98ee-7c105dec6852.jpg)

## Authors

- [@Atanu Roy](https://github.com/Mr-Atanu-Roy)
- [@Ricky](https://github.com/Ricky2054)
- [@Sagarika](https://github.com/Sagarika-02)
- [@Sayanika](https://github.com/Sayanika19)


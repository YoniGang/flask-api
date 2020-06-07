# Flask messaging API

API for messaging service application with auth

The API server runs at: [https://warm-ocean-40786.herokuapp.com/](https://warm-ocean-40786.herokuapp.com/)

You can see API using examples at: [Postman calls examples](https://web.postman.co/collections/4016156-680b2ded-94f2-4343-a218-643dbaa40430?workspace=d801c19e-93aa-4b85-856e-2b9aefac5cb9)

# Instructions

## Send message

To send message, user must be logged in, and the receiver must be registered to the db

## Read all messages and unread messages

User must be logged in, and the user will get all messages where he was the receiver

## Read or Delete message

To read or delete specific message, the user must be logged in and the user must be the sender or the receiver

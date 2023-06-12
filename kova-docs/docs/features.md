# Features

## Applicative server

- Server uses Routers to process the messages in the queue
- A Router is linked to a NATS queue
- Use of protobuf messages to encapsulate NATS messages (see [Messages example](messages.md) for further details))

## NATS Clients

- Connected to the NATS server
- Use of publish/subscribe and request/reply to interact with both the applicative server and other clients
- Some client examples :
    * Identified echo : Dialogue between an identified client and the applicative server
    * Ping Pong : Conversation between 2 identified clients

## Authentication service

- Service uses JWT authentication
- API with two endpoints :
    * `/register` : Save user email and ID in database
    * `/login` : Create user credentials using the NSC Service


## NSC Service and Wrapper

- NSC Wrapper is a Python wrapper that calls the nsc library
    * Used to create NATS Operator, Account and User
- NSC Service is an API used to set up a new Operator and Account when creating a new system
- NSC Service is also called during user creation

!!! note
    You can change the default file in which the users keys and credentials are saved through the `NscSettings`.

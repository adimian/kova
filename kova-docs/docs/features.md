# Features

## Applicative server

- Server uses Routers to process the messages in the queue
- A Router is subscribed to a NATS queue and will get all messages through it
- Use of protobuf messages to encapsulate NATS messages (see [Messages example](messages.md) for further details)

## NATS Clients

- Connected to the NATS server
- Use of Publish/Subscribe and Request/Reply message distribution model to interact with both the applicative server and other clients
- Some client examples :
    * Identified echo : Dialogue between an identified client and the applicative server
    * Caching echo : Dialogue between a client and a server, the message is cached for 5s
    * Ping Pong : Conversation between 2 clients
    * Sending files : Use of MinIO to send images and modify them in the applicative server

## Authentication service

- Service uses JWT authentication
- API with two endpoints :
    * `/register` : Save user email and ID in database
    * `/login` : Create user credentials using the NSC Service
- Credentials are valid for 6 months by default (can be changed through `NscSettings`)
- Credentials define both the identity of the client thanks to its keys but also the authorization given (which queues can a client post and listen on)


## NSC Service and Wrapper

- NSC Wrapper is a Python wrapper that calls the `nsc` library
    * Used to create NATS Operator, Account and User
- NSC Service is an API used to set up a new Operator and Account when creating a new system
- NSC Service is also called during user creation, this service effectively creates user private and public keys as well as their credentials

!!! note
    You can change the default file in which the users keys and credentials are saved through the `NscSettings`.

## Persistent messaging

- NATS Jetstream is a service that allows server side persistence once enabled on the NATS server
- The Buffer allows for client side persistence by saving unsent messages in case of errors (see [Persistence example](persistence.md) for further details)
- Some client examples :
    * Stream echo : Dialogue between an identified client and the applicative server using all persistence features

# First register

## Happy path
```mermaid
sequenceDiagram
    Client ->> Web_Server: LoginRequest(email)
    Web_Server ->> Database: Insert(User_ULID, email)
```

## Error handling

### Email already registered
```mermaid
sequenceDiagram
    Client ->> Web_Server: LoginRequest(email)
    Web_Server ->> Database: Insert(User_ULID, email)
    Database ->> Web_Server: Error("Email already registered")
    Web_Server ->> Client : Error("Email already registered")
```

# Obtaining a `JWT`

## Happy path
```mermaid
sequenceDiagram
    Client ->> Web_Server: Login(email)
    Web_Server ->> Applicative_Server: Config_user_access (using nsc)
    Applicative_Server ->> Client: Credentials(jwt, seed)
```
## Error handling

### Invalid email
```mermaid
sequenceDiagram
    Client ->> Web_Server: Login(email)
    Web_Server ->> Client: Error("Invalid email, not saved in DB")

```

# Making authenticated calls

## Happy path
```mermaid
sequenceDiagram
    Client ->> NATS_Server: PerformAction({headers: credentials}, [params,...])
    NATS_Server ->> Client: Response([data, ...])
```

## Error handling

### Invalid Credentials
```mermaid
sequenceDiagram
    Client ->> NATS_Server: PerformAction({headers: credentials}, [params,...])
    NATS_Server ->> Client: Error("Invalid credentials")
```

### Missing Credentials
```mermaid
sequenceDiagram
    Client ->> NATS_Server: PerformAction({headers: credentials}, [params,...])
    NATS_Server ->> Client: Error("Missing credentials")
```

### No longer valid Credentials
```mermaid
sequenceDiagram
    Client ->> NATS_Server: PerformAction({headers: credentials}, [params,...])
    NATS_Server ->> Client: Error("Credentials have expired, Login again")
```

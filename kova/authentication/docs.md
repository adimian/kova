# First register

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Database: Insert(User_ULID, email)
```

## Error handling

### Email already registered
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Database: Insert(User_ULID, email)
    Database ->> Server: Error("Email already registered")
    Server ->> Client : Error("Email already registered")
```

# Obtaining a `JWT`

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: Login(email)
    Server ->> Server: Config_user_access (using nsc)
    Server ->> Client: Credentials(jwt, seed)
```
## Error handling

### Invalid email
```mermaid
sequenceDiagram
    Client ->> Server: Login(email)
    Server ->> Client: Error("Invalid email, not saved in DB")

```

# Making authenticated calls

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: credentials}, [params,...])
    Server ->> Client: Response([data, ...])
```

## Error handling

### Invalid Credentials
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: credentials}, [params,...])
    Server ->> Client: Error("Invalid credentials")
```

### Missing Credentials
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: credentials}, [params,...])
    Server ->> Client: Error("Missing credentials")
```

### No longer valid Credentials
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: credentials}, [params,...])
    Server ->> Client: Error("Credentials have expired, Login again")
```

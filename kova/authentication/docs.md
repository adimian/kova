# Obtaining a `refresh_token`

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Client ->> Server: LoginSessionRequest(session_code)
    alt has_mfa_enabled
    Server ->> Client: LoginResponse(mfa_required)
    Client ->> Server: LoginSessionRequest(session_code, mfa_code)
    end
    Server ->> Client: LoginResponse(refresh_token)
```

## Error handling
TODO

# Obtaining an `access_token`

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: AccessToken(access_token)
```
## Error handling
TODO

# Making authenticated calls

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Response([data, ...])
```

## Error handling
TODO

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

### wrong email
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Mail Service ->> Server: Error : invalid email
    Server ->> Client : Error : invalid email... try again !
```

### mfa : wrong phone number
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Client ->> Server: LoginSessionRequest(session_code)
    alt has_mfa_enabled
    loop wrong_number
    Server ->> Client: LoginResponse(mfa_required)
    end
    Client ->> Server: LoginSessionRequest(session_code, mfa_code)
    end
    Server ->> Client: LoginResponse(refresh_token)
```

### session_code invalid
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Client ->> Server: LoginSessionRequest(session_code)
    alt has_mfa_enabled
    Server ->> Client: LoginResponse(mfa_required)
    Client ->> Server: LoginSessionRequest(session_code, mfa_code)
    end
    Server ->> Client: error : invalid session_code
```


# Obtaining an `access_token`

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: AccessToken(access_token)
```
## Error handling

### invalid token
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: Error : invalid_token
```

### missing token
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: Error : invalid_request
```

# Making authenticated calls

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Response([data, ...])
```

## Error handling

### invalid token
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Error : invalid_token
```

### missing token
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Error : missing_token
```

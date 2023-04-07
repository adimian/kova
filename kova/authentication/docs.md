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

```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, refresh_token/temporary mdp)
    Client ->> Server: AccessTokenRequest(refresh_token/temporary mdp)
    Server ->> Server: Verify refresh_token validity
    Server ->> Server: Creation of user
    Server ->> Client: AccessToken(seed/credentials)

```

## Error handling

### Invalid email
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Mail Service ->> Server: Error("invalid email")
    Server ->> Client : Error("invalid email")
```

### MFA : wrong phone number
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

### Invalid session_code
```mermaid
sequenceDiagram
    Client ->> Server: LoginRequest(email)
    Server ->> Mail Service: send_session_code(email, session_code)
    Client ->> Server: LoginSessionRequest(session_code)
    alt has_mfa_enabled
    Server ->> Client: LoginResponse(mfa_required)
    Client ->> Server: LoginSessionRequest(session_code, mfa_code)
    end
    Server ->> Client: Error("invalid session_code")
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

### Invalid refresh token
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: Error("invalid_refresh_token")
```

### Missing refresh token
```mermaid
sequenceDiagram
    Client ->> Server: AccessTokenRequest(refresh_token)
    Server ->> Server: Verify refresh_token validity
    Server ->> Client: Error("missing_refresh_token")
```

# Making authenticated calls

## Happy path
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Response([data, ...])
```

## Error handling

### Invalid access token
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Error("invalid_access_token")
```

### Missing access token
```mermaid
sequenceDiagram
    Client ->> Server: PerformAction({headers: access_token}, [params,...])
    Server ->> Client: Error("missing_access_token")
```

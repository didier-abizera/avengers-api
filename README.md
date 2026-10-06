# Secure the Movie Franchise: Avengers API (Basic Auth)

## What I built
A Python server (`http.server`) with one protected endpoint:
`GET /movies/avengers`, which returns the Avengers movie list as JSON.
It uses HTTP Basic Auth. The server decodes the `Authorization` header
and checks the username and password against a `USERS` dictionary.

## QA tests (Tester role)

| # | Test | Command | Expected | Result |
|---|------|---------|----------|--------|
| 1 | Valid user | `-u admin:secret` | 200 | Pass |
| 2 | Wrong password | `-u admin:wrongpass` | 401 | Pass |
| 3 | No credentials | (none) | 401 | Pass |
| 4 | Unknown user | `-u hacker:abc` | 401 | Pass |

## Attack attempts

| Attack | Command | Expected | Result |
|--------|---------|----------|--------|
| Garbage base64 | `Authorization: Basic !!!notbase64!!!` | 401, no crash | Pass |
| Wrong auth type | `Authorization: Bearer abc123` | 401 | Pass |
| Empty password | `-u admin:` | 401 | Pass |
| Valid login, wrong path | `-u admin:secret /movies/hacked` | 404 | (add your result) |

## Findings and fixes

1. **Server freezes when one connection stays open.**
   The server handled one request at a time, so one idle connection (Chrome
   kept one open) blocked every other request. This is a denial-of-service risk.
   *Fix:* changed `HTTPServer` to `ThreadingHTTPServer`, so each request
   gets its own thread.

2. **Garbage input could crash the server.**
   Bad base64 or a login with no `:` would raise an error.
   *Fix:* wrapped the decoding in `try/except` so bad input returns 401.

3. **Unknown username could raise an error.**
   *Fix:* used `USERS.get(username)`, which returns `None` instead of crashing.

## Remaining risks (not fixed here)
- Basic Auth is base64 encoding, not encryption. In production it must run over HTTPS.
- Passwords are hardcoded in the source code. A real app would use hashed passwords.
- There is no limit on login attempts, so a password could be guessed repeatedly.

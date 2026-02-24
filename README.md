# UserManagementAPI (.NET 8 + MongoDB)

This project implements the requirements from `Code-Gen-Requirement.txt`:

- User registration with validation
- Login/logout with error handling
- Forgot password (token + reset link plumbing point)
- Save personal info with field validations
- List of top 10 food preferences
- MongoDB for persistence
- Password hashing (BCrypt) and basic rate limiting

## Structure

```
/ src/UserManagementAPI            # ASP.NET Core Web API project
/ tests/UserManagementAPI.Tests    # xUnit tests
/ .github/workflows/dotnet.yml     # CI: build and tests
UserManagement.sln                 # Solution
```

## Configuration

The API expects the MongoDB connection string from the environment variable `MONGODB_URI`. In development, `launchSettings.json` sets:

```
MONGODB_URI = mongodb://localhost:27017/UserManagementDB
```

In production/CI, provide this via environment or GitHub Secret.

### GitHub Secret: MONGODB_URI

Set a repository secret so CI and deployments can access it.

1. Go to GitHub repo → Settings → Secrets and variables → Actions → New repository secret
2. Name: `MONGODB_URI`
3. Value: e.g. `mongodb+srv://<user>:<password>@<cluster>/<database>?retryWrites=true&w=majority`

The CI workflow consumes it during `dotnet test`.

## Run locally

- .NET 8 SDK required

```
cd src/UserManagementAPI
 dotnet restore
 dotnet run
```

API will start on:
- https://localhost:7243
- http://localhost:5243

## Docker

Build and run the API in Docker:

```
docker build -t usermgmt-api:latest -f src/UserManagementAPI/Dockerfile .
docker run -e MONGODB_URI="mongodb://host.docker.internal:27017/UserManagementDB" -p 8080:8080 usermgmt-api:latest
```

## Endpoints (high level)

- POST `/register` – email/phone + password + confirm + security question; validations enforced
- POST `/forgot-password` – verifies security question answer, emits reset token (wire up email/SMS)
- POST `/login` – returns success or error
- POST `/logout`
- GET `/api/user/food-preferences` – returns top 10 types
- POST `/api/user/personal-info` – name, age, sex, address, profile picture; validations enforced

## Notes

- Passwords are stored as hashes (BCrypt)
- Basic rate limiting applied to sensitive endpoints
- Add your email/SMS provider for sending password reset links
- Supply `MONGODB_URI` via env or GitHub Secrets; `appsettings.json` contains only a placeholder

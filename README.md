# User Management API (.NET 8 + MongoDB)

Implements the requirements from Code-Gen-Requirement.txt:
- Registration via email or phone with validation
- Login/logout
- Forgot password using security question (sends reset link placeholder)
- Save personal information with validation
- Provide top 10 food preferences
- Persist all data in MongoDB

## Tech
- .NET 8 (ASP.NET Core Web API)
- MongoDB (MongoDB.Driver)
- Password hashing with BCrypt
- Basic rate limiting for auth endpoints

## Setup
1. Prerequisites: .NET 8 SDK, MongoDB instance/Atlas connection string.
2. Clone repo and navigate to `src/UserManagementAPI`.
3. Configure connection string:
   - Prefer environment variable `MONGODB_URI`.
   - Or edit `appsettings.json` (placeholder is present). Avoid committing real secrets.
4. Run:
   - `dotnet restore`
   - `dotnet build`
   - `dotnet run`
5. API base: `https://localhost:5001` (or `http://localhost:5000`).

## Endpoints
- POST `/api/auth/register` — Register with Email or Phone, Password/Confirm, SecurityQuestion, SecurityAnswer.
- POST `/api/auth/login` — Login with EmailOrPhone + Password. Returns 200 on success, 400 on invalid.
- POST `/api/auth/forgot-password` — Verify SecurityAnswer and (placeholder) send reset link.
- POST `/api/auth/logout` — Stateless placeholder returns 200.
- POST `/api/user/personal-info` — Save Name, Age, Sex (Male/Female), Address, ProfilePicture, optional FoodPreferences for a user identified by EmailOrPhone.
- GET `/api/user/food-preferences` — Returns the top 10 food types.

## Security
- Passwords and security answers are hashed (BCrypt).
- Basic rate limiting on `/login` and `/forgot-password`.

## Configuration
- Database name default: `UserManagementDB`.
- Collections: `Users`, `PasswordResetTokens`.

## Notes
- Email/SMS sending for password reset is a placeholder to be wired to a provider.
- For production, add proper authentication (e.g., JWT), HTTPS, and secret storage (GitHub Secrets, Key Vault, etc.).

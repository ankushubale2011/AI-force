# Customer Survey Program

## Overview
This application manages an end-to-end customer survey lifecycle with three roles:
1. **Lead Manager**
2. **Center of Excellence (CoE)**
3. **Customer**

### Features & Workflow:
- Lead Manager creates a survey with questions/parameters, dates, and customer mapping, then submits for CoE review.
- CoE reviews survey details and can approve, reject, or request changes.
- Once approved, the survey is published and sent to customers via portal and optional email notification.
- Customers open survey link, fill in parameters/questions, save progress, and submit the final response.
- The system tracks status, sends notifications, keeps an audit trail, and enables reporting/exports for internal stakeholders.

## Technology Stack
- **UI:** Angular
- **Middleware:** .NET Core
- **Database:** MS SQL 2022

## Project Structure
```
/backend
  Controllers/
  Services/
  Models/
  Constants/
  Data/
  schema.sql
/frontend
  src/app/
    survey/
      survey.service.ts
      survey.component.ts
```

## Setup Instructions

### Backend (.NET Core)
1. Install .NET Core SDK.
2. Navigate to `/backend`.
3. Restore dependencies:
   ```bash
   dotnet restore
   ```
4. Update `appsettings.json` with your database connection string.
5. Apply migrations and update database:
   ```bash
   dotnet ef database update
   ```
6. Run the backend:
   ```bash
   dotnet run
   ```

### Database (MS SQL 2022)
1. Create a new database.
2. Execute the `schema.sql` script in `/backend`.

### Frontend (Angular)
1. Install Node.js and Angular CLI.
2. Navigate to `/frontend`.
3. Install dependencies:
   ```bash
   npm install
   ```
4. Run frontend:
   ```bash
   ng serve
   ```
5. Open browser at `http://localhost:4200`

## Deployment
- Ensure both frontend and backend are hosted, with backend API endpoint properly configured in Angular's environment files.

## Auth & Roles
- Implement authentication/authorization with role checks in backend controllers and frontend routing guards.


# Build and run UserManagementAPI (.NET 8)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 8080
ENV ASPNETCORE_URLS=http://+:8080

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/UserManagementAPI/UserManagementAPI.csproj", "src/UserManagementAPI/"]
RUN dotnet restore "src/UserManagementAPI/UserManagementAPI.csproj"
COPY . .
WORKDIR "/src/src/UserManagementAPI"
RUN dotnet publish "UserManagementAPI.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
# MONGODB_URI should be injected at runtime (e.g., via Docker env or Kubernetes secret)
ENV MONGODB_URI=""
ENTRYPOINT ["dotnet", "UserManagementAPI.dll"]

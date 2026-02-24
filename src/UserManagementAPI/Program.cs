using Microsoft.AspNetCore.RateLimiting;
using MongoDB.Driver;
using System.Threading.RateLimiting;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllers();

// Basic rate limiting policy for auth endpoints
builder.Services.AddRateLimiter(options =>
{
    options.RejectionStatusCode = StatusCodes.Status429TooManyRequests;
    options.AddPolicy("auth", httpContext =>
        RateLimitPartition.GetIpPartition(httpContext, ip =>
            new TokenBucketRateLimiterOptions
            {
                TokenLimit = 10,
                TokensPerPeriod = 10,
                ReplenishmentPeriod = TimeSpan.FromMinutes(1),
                QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
                QueueLimit = 0,
                AutoReplenishment = true
            }));
});

// MongoDB configuration: prefer env var MONGODB_URI, otherwise appsettings
var connStr = Environment.GetEnvironmentVariable("MONGODB_URI")
             ?? builder.Configuration.GetSection("MongoDB").GetValue<string>("ConnectionString")
             ?? "mongodb://localhost:27017";
var databaseName = builder.Configuration.GetSection("MongoDB").GetValue<string>("Database") ?? "UserManagementDB";

builder.Services.AddSingleton<IMongoClient>(_ => new MongoClient(connStr));
builder.Services.AddSingleton(sp =>
{
    var client = sp.GetRequiredService<IMongoClient>();
    return client.GetDatabase(databaseName);
});

var app = builder.Build();

// Configure the HTTP request pipeline.
app.UseHttpsRedirection();
app.UseRateLimiter();
app.MapControllers();

app.Run();

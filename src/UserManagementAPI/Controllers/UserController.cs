using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using MongoDB.Driver;
using UserManagementAPI.Models;
using UserManagementAPI.DTOs;

namespace UserManagementAPI.Controllers
{
    [ApiController]
    [Route("api/user")]
    public class UserController : ControllerBase
    {
        private readonly IMongoCollection<User> _users;
        private static readonly List<string> FoodTypes = new()
        {
            "Indian","Chinese","French","Italian","Mexican",
            "Japanese","Thai","American","Greek","Mediterranean"
        };

        public UserController(IConfiguration config)
        {
            var conn = Environment.GetEnvironmentVariable("MONGODB_URI")
                       ?? config.GetConnectionString("MongoDb")
                       ?? config["MongoDb:ConnectionString"]
                       ?? "mongodb://localhost:27017/UserManagementDB";
            var mongoUrl = new MongoUrl(conn);
            var client = new MongoClient(mongoUrl);
            var db = client.GetDatabase(!string.IsNullOrWhiteSpace(mongoUrl.DatabaseName) ? mongoUrl.DatabaseName : "UserManagementDB");
            _users = db.GetCollection<User>("Users");
        }

        [HttpGet("food-preferences")]
        public ActionResult<IEnumerable<string>> GetFoodPreferences()
        {
            return Ok(FoodTypes);
        }

        [HttpPost("personal-info")]
        public IActionResult SavePersonalInfo([FromBody] PersonalInfoRequest request)
        {
            if (request == null)
                return BadRequest("Request body is required.");

            if (string.IsNullOrWhiteSpace(request.Email) || !IsValidEmailOrPhone(request.Email))
                return BadRequest("Invalid email address or phone number.");

            if (!IsValidName(request.Name))
                return BadRequest("Invalid name. Name should be at least 2 characters and contain only letters and spaces.");

            if (!IsValidAge(request.Age))
                return BadRequest("Age must be between 18 and 99.");

            if (!IsValidSex(request.Sex))
                return BadRequest("Sex must be either 'Male' or 'Female'.");

            if (!IsValidAddress(request.Address))
                return BadRequest("Invalid address. Address should be at least 5 characters and contain only letters, numbers, and spaces.");

            var filter = Builders<User>.Filter.Eq(u => u.Email, request.Email);
            var update = Builders<User>.Update
                .Set(u => u.Name, request.Name)
                .Set(u => u.Age, request.Age)
                .Set(u => u.Sex, request.Sex)
                .Set(u => u.Address, request.Address)
                .Set(u => u.ProfilePicture, request.ProfilePicture);

            var result = _users.UpdateOne(filter, update);
            if (result.MatchedCount == 0)
            {
                return BadRequest("User not found. Please register first.");
            }

            return Ok("User personal information saved successfully.");
        }

        private static bool IsValidEmail(string email)
        {
            try
            {
                var addr = new System.Net.Mail.MailAddress(email);
                return addr.Address == email;
            }
            catch { return false; }
        }

        private static bool IsValidPhone(string phone)
        {
            return Regex.IsMatch(phone ?? string.Empty, @"^\d{3}-\d{3}-\d{4}$");
        }

        private static bool IsValidEmailOrPhone(string value)
        {
            return IsValidEmail(value) || IsValidPhone(value);
        }

        private static bool IsValidName(string name)
        {
            if (string.IsNullOrWhiteSpace(name) || name.Trim().Length < 2) return false;
            return Regex.IsMatch(name.Trim(), @"^[A-Za-z ]+$");
        }

        private static bool IsValidAge(int age)
        {
            return age >= 18 && age <= 99;
        }

        private static bool IsValidSex(string sex)
        {
            return string.Equals(sex, "Male", StringComparison.OrdinalIgnoreCase)
                || string.Equals(sex, "Female", StringComparison.OrdinalIgnoreCase);
        }

        private static bool IsValidAddress(string address)
        {
            if (string.IsNullOrWhiteSpace(address) || address.Trim().Length < 5) return false;
            return Regex.IsMatch(address.Trim(), @"^[A-Za-z0-9 ]+$");
        }
    }
}

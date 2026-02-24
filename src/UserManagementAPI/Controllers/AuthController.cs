using BCrypt.Net;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.RateLimiting;
using MongoDB.Driver;
using System.Security.Cryptography;
using UserManagementAPI.DTOs;
using UserManagementAPI.Models;
using UserManagementAPI.Utils;

namespace UserManagementAPI.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly IMongoCollection<User> _users;
        private readonly IMongoCollection<PasswordResetToken> _resetTokens;

        public AuthController(IMongoDatabase database)
        {
            _users = database.GetCollection<User>("Users");
            _resetTokens = database.GetCollection<PasswordResetToken>("PasswordResetTokens");
        }

        [HttpPost("register")]
        public async Task<IActionResult> Register([FromBody] RegistrationRequest req)
        {
            if ((string.IsNullOrWhiteSpace(req.Email) && string.IsNullOrWhiteSpace(req.Phone)) ||
                (!string.IsNullOrWhiteSpace(req.Email) && !string.IsNullOrWhiteSpace(req.Phone)))
            {
                return BadRequest("Provide either a valid email address or a valid phone number (but not both).");
            }

            if (!string.IsNullOrWhiteSpace(req.Email) && !ValidationUtils.IsValidEmail(req.Email!))
                return BadRequest("Invalid email address");

            if (!string.IsNullOrWhiteSpace(req.Phone) && !ValidationUtils.IsValidPhone(req.Phone!))
                return BadRequest("Invalid phone number");

            if (req.Password != req.ConfirmPassword)
                return BadRequest("Passwords do not match.");

            if (!ValidationUtils.IsValidPassword(req.Password))
                return BadRequest("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character.");

            if (string.IsNullOrWhiteSpace(req.SecurityQuestion) || string.IsNullOrWhiteSpace(req.SecurityAnswer))
                return BadRequest("Security question and answer are required.");

            // Uniqueness check
            if (!string.IsNullOrWhiteSpace(req.Email))
            {
                var exists = await _users.Find(u => u.Email == req.Email).AnyAsync();
                if (exists) return Conflict("Email already registered.");
            }
            if (!string.IsNullOrWhiteSpace(req.Phone))
            {
                var exists = await _users.Find(u => u.Phone == req.Phone).AnyAsync();
                if (exists) return Conflict("Phone already registered.");
            }

            var user = new User
            {
                Email = req.Email,
                Phone = req.Phone,
                PasswordHash = BCrypt.Net.BCrypt.HashPassword(req.Password),
                SecurityQuestion = req.SecurityQuestion,
                SecurityAnswerHash = BCrypt.Net.BCrypt.HashPassword(req.SecurityAnswer)
            };

            await _users.InsertOneAsync(user);
            return Ok("User registered successfully.");
        }

        [HttpPost("login")]
        [EnableRateLimiting("auth")]
        public async Task<IActionResult> Login([FromBody] LoginRequest req)
        {
            if (string.IsNullOrWhiteSpace(req.EmailOrPhone) || string.IsNullOrWhiteSpace(req.Password))
                return BadRequest("Email or phone and password are required.");

            var byEmail = req.EmailOrPhone.Contains('@');
            User? user = byEmail
                ? await _users.Find(u => u.Email == req.EmailOrPhone).FirstOrDefaultAsync()
                : await _users.Find(u => u.Phone == req.EmailOrPhone).FirstOrDefaultAsync();

            if (user == null || !BCrypt.Net.BCrypt.Verify(req.Password, user.PasswordHash))
                return BadRequest("Incorrect email or password");

            // Normally return a token/session. Here we just acknowledge success.
            return Ok("User logged in successfully.");
        }

        [HttpPost("forgot-password")]
        [EnableRateLimiting("auth")]
        public async Task<IActionResult> ForgotPassword([FromBody] ForgotPasswordRequest req)
        {
            if (string.IsNullOrWhiteSpace(req.EmailOrPhone) || string.IsNullOrWhiteSpace(req.SecurityAnswer))
                return BadRequest("Email or phone and security answer are required.");

            var byEmail = req.EmailOrPhone.Contains('@');
            User? user = byEmail
                ? await _users.Find(u => u.Email == req.EmailOrPhone).FirstOrDefaultAsync()
                : await _users.Find(u => u.Phone == req.EmailOrPhone).FirstOrDefaultAsync();

            if (user == null)
                return BadRequest("Incorrect security question answer.");

            if (!BCrypt.Net.BCrypt.Verify(req.SecurityAnswer, user.SecurityAnswerHash))
                return BadRequest("Incorrect security question answer.");

            // Create a reset token and (placeholder) send via email/SMS
            var token = Convert.ToHexString(RandomNumberGenerator.GetBytes(32));
            var record = new PasswordResetToken
            {
                UserId = user.Id!,
                Token = token,
                ExpiresAt = DateTime.UtcNow.AddHours(1)
            };
            await _resetTokens.InsertOneAsync(record);

            // TODO: Integrate with email/SMS provider to send the link containing the token
            // For now, we simply return a generic message without exposing the token.
            return Ok("Password reset link sent.");
        }

        [HttpPost("logout")]
        public IActionResult Logout()
        {
            // Stateless API placeholder
            return Ok("User logged out successfully.");
        }
    }
}

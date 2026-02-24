namespace UserManagementAPI.DTOs
{
    public class RegistrationRequest
    {
        public string? Email { get; set; }
        public string? Phone { get; set; }
        public string Password { get; set; } = string.Empty;
        public string ConfirmPassword { get; set; } = string.Empty;
        public string SecurityQuestion { get; set; } = string.Empty;
        public string SecurityAnswer { get; set; } = string.Empty;
    }
}

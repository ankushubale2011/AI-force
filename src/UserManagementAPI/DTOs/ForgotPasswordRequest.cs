namespace UserManagementAPI.DTOs
{
    public class ForgotPasswordRequest
    {
        public string EmailOrPhone { get; set; } = string.Empty;
        public string SecurityAnswer { get; set; } = string.Empty;
    }
}

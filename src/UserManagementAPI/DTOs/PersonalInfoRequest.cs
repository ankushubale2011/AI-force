using System.Collections.Generic;

namespace UserManagementAPI.DTOs
{
    public class PersonalInfoRequest
    {
        public string EmailOrPhone { get; set; } = string.Empty;
        public string Name { get; set; } = string.Empty;
        public int Age { get; set; }
        public string Sex { get; set; } = string.Empty; // "Male" or "Female"
        public string Address { get; set; } = string.Empty;
        public string? ProfilePicture { get; set; }
        public List<string>? FoodPreferences { get; set; }
    }
}

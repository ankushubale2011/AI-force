using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System.Collections.Generic;

namespace UserManagementAPI.Models
{
    public class User
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }

        public string? Email { get; set; }
        public string? Phone { get; set; }

        public string PasswordHash { get; set; } = string.Empty;

        public string SecurityQuestion { get; set; } = string.Empty;
        public string SecurityAnswerHash { get; set; } = string.Empty;

        public string? Name { get; set; }
        public int? Age { get; set; }
        public string? Sex { get; set; }
        public string? Address { get; set; }
        public string? ProfilePicture { get; set; }

        public List<string> FoodPreferences { get; set; } = new();
    }
}

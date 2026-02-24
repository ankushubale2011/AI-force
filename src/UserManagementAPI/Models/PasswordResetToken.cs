using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;
using System;

namespace UserManagementAPI.Models
{
    public class PasswordResetToken
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string? Id { get; set; }

        [BsonRepresentation(BsonType.ObjectId)]
        public string UserId { get; set; } = string.Empty;

        public string Token { get; set; } = string.Empty;
        public DateTime ExpiresAt { get; set; }
        public bool Consumed { get; set; } = false;
    }
}

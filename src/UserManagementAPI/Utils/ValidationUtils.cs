using System.Text.RegularExpressions;

namespace UserManagementAPI.Utils
{
    public static class ValidationUtils
    {
        public static bool IsValidEmail(string email)
        {
            try
            {
                var addr = new System.Net.Mail.MailAddress(email);
                return addr.Address == email;
            }
            catch { return false; }
        }

        public static bool IsValidPhone(string phone)
        {
            return Regex.IsMatch(phone, @"^\d{3}-\d{3}-\d{4}$");
        }

        public static bool IsValidPassword(string password)
        {
            if (string.IsNullOrEmpty(password) || password.Length < 8) return false;
            bool hasUpper = Regex.IsMatch(password, @"[A-Z]");
            bool hasLower = Regex.IsMatch(password, @"[a-z]");
            bool hasDigit = Regex.IsMatch(password, @"\d");
            bool hasSpecial = Regex.IsMatch(password, @"[^A-Za-z0-9]");
            return hasUpper && hasLower && hasDigit && hasSpecial;
        }

        public static bool IsValidName(string name)
        {
            return Regex.IsMatch(name, @"^[A-Za-z]{2,}$");
        }

        public static bool IsValidSex(string sex)
        {
            return sex == "Male" || sex == "Female";
        }

        public static bool IsValidAddress(string address)
        {
            return address.Length >= 5 && Regex.IsMatch(address, @"^[A-Za-z0-9 ]+$");
        }
    }
}

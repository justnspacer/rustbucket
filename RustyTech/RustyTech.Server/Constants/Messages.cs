namespace RustyTech.Server.Constants
{
    public class Messages
    {
        // Required Fields
        public const string EmailRequired = "Email is required";
        public const string IdRequired = "ID is required";
        public const string PasswordRequired = "Password is required";

        // Info Messages
        public static class Info
        {
            public const string ResendEmail = "Resend confirmation email sent";
            public const string UserLoggedIn = "User logged in";
            public const string UserLoggedOut = "User logged out";
            public const string UserNotFound = "User not found";
            public const string UserNotVerified = "User not verified";
            public const string UserPasswordReset = "User password reset code created, please check email";
            public const string UserPasswordChanged = "User password changed, please check email";
            public const string UserExists = "User already exists";
            public const string UserRegistered = "User registered, please check email for confirmation";
            public const string PasswordReset = "Password can be reset";
            public const string UserDeleted = "User deleted";
            public const string PostCreated = "Post created";
            public const string PostNotFound = "Post not found";
            public const string PostUpdated = "Post updated";
        }

        // Role Messages
        public static class Role
        {
            public const string NameRequired = "Role name is required";
            public const string Created = "Role created";
            public const string Exists = "Role already exists";
            public const string NotFound = "Role not found";
            public const string Removed = "Role removed";
            public const string AddedToUser = "Role added to user";
        }

        // Error Messages
        public static class Error
        {
            public const string DataRecheck = "Please recheck input data";
            public const string ErrorConfirmingEmail = "Error confirming email";
            public const string InvalidCredentials = "Invalid credentials";
            public const string InvalidRequest = "Invalid request";
            public const string BadRequest = "Bad request";
            public const string PasswordError = "Password must contain at least 6 characters, one lowercase letter, one uppercase letter, one digit, and one special character";
            public const string PasswordMismatch = "Password and confirm password mismatch";
            public const string InvalidEmail = "Invaild email";
            public const string Unauthorized = "Unauthorized";
            public const string RecheckEmailPassword = "Please recheck email and password";
        }

        // Token Messages
        public static class Token
        {
            public const string Invalid = "Invalid Token";
            public const string Expired = "Token expired";
            public const string Required = "Token is required";
            public const string Valid = "Valid token";
        }
    }
}

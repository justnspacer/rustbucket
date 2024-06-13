namespace RustyTech.Server.Constants
{
    public class Message
    {
        //Required Fields
        public const string EmailRequired = "Email is required";
        public const string IdRequried = "Id is required";
        public const string PasswordRequired = "Password is required";

        //Info Messages
        public const string ResendEmail = "Resend confirmation email sent";
        public const string UserLoggedIn = "User logged in";
        public const string UserLoggedOut = "User logged out";
        public const string UserNotFound = "User not found";
        public const string UserNotVerified = "User not verified";
        public const string UserPassword = "User password reset, please check email";
        public const string UserExists = "User already exists";
        public const string UserRegistered = "User registered, please check email for confirmation";
        public const string PasswordReset = "Password can be reset";

        //Error Messages
        public const string DataRecheck = "Please recheck input data";
        public const string ErrorConfirmingEmail = "Error confirming email";
        public const string InvalidCredentials = "Invalid credentials";
        public const string InvalidRequest = "Invalid request";
        public const string PasswordError = "Password must contain at least 6 characters, one lowercase letter, one uppercase letter, one digit, and one special character";
        public const string PasswordMismatch = "Password and confirm password mismatch";


        //Token Messages
        public const string InvalidToken = "Invalid Token";
        public const string TokenExpired = "Token expired";
        public const string TokenNotFound = "Token not found";
        public const string ValidToken = "Valid Token";
    }
}

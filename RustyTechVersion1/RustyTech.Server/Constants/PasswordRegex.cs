namespace RustyTech.Server.Constants
{
    public class PasswordRegex
    {
        public const string Pattern = @"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{6,}$";
    }
}

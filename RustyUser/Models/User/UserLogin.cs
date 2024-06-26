﻿namespace RustyUser.Models.User
{
    public class UserLogin
    {
        public required string Email { get; set; }
        public required string Password { get; set; }
        public bool RememberMe { get; set; }
        public string? ApplicationName { get; set; }
        public string LoginProvider { get; set; } = string.Empty;
        public string ProviderKey { get; set; } = string.Empty;
    }
}

﻿namespace RustyTech.Server.Models.Role
{
    public class RoleRequest
    {
        public string? RoleId { get; set; }
        public Guid UserId { get; set; }
    }
}

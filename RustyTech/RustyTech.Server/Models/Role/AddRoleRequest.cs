﻿namespace RustyTech.Server.Models.Role
{
    public class AddRoleRequest
    {
        public string? Id { get; set; }
        public string? RoleName { get; set; }
        public Guid UserId { get; set; }
    }
}

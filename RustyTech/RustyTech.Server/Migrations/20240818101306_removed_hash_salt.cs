using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class removed_hash_salt : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.InsertData(
                table: "AspNetUsers",
                columns: new[] { "Id", "AccessFailedCount", "BirthYear", "ConcurrencyStamp", "Email", "EmailConfirmed", "LockoutEnabled", "LockoutEnd", "NormalizedEmail", "NormalizedUserName", "PasswordHash", "PasswordResetToken", "PhoneNumber", "PhoneNumberConfirmed", "ResetTokenExpires", "SecurityStamp", "TwoFactorEnabled", "UserName", "VerificationToken", "VerifiedAt" },
                values: new object[] { "b5e225b0-489d-4757-b266-bfdf41d7c308", 0, 0, "fbe865c7-93a0-4198-82b7-58ad9cc0dfd7", "admin@rustbucket.io", true, false, null, "ADMIN@RUSTBUCKET.IO", "ADMIN@RUSTBUCKET.IO", "JackNJill1!", null, null, false, null, "3cf30978-a0aa-4888-b7cf-a66cf4ffe2b3", false, "admin@rustbucket.io", null, new DateTime(2024, 8, 18, 4, 57, 11, 782, DateTimeKind.Local).AddTicks(2521) });

            migrationBuilder.InsertData(
                table: "AspNetRoles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "1", "1", "SuperAdmin", "SUPERADMINISTRATOR" });


            migrationBuilder.InsertData(
                table: "AspNetUserRoles",
                columns: new[] { "RoleId", "UserId" },
                values: new object[] { "1", "b5e225b0-489d-4757-b266-bfdf41d7c308" });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "AspNetUserRoles",
                keyColumns: new[] { "RoleId", "UserId" },
                keyValues: new object[] { "1", "b5e225b0-489d-4757-b266-bfdf41d7c308" });

            migrationBuilder.DeleteData(
                table: "AspNetUsers",
                keyColumn: "Id",
                keyValue: "b5e225b0-489d-4757-b266-bfdf41d7c308");

            migrationBuilder.DeleteData(
                table: "AspNetRoles",
                keyColumn: "Id",
                keyValue: "1");
        }
    }
}

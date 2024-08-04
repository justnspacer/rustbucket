using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class admin_reseeding : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
    name: "UserRoles",
    columns: table => new
    {
        Id = table.Column<int>(type: "int", nullable: false).Annotation("SqlServer:Identity", "1, 1"),
        RoleId = table.Column<string>(type: "nvarchar(max)", nullable: true),
        UserId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
        CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false)
    },
    constraints: table =>
    {
        table.PrimaryKey("PK_UserRoles", x => x.Id);
    });
            migrationBuilder.DeleteData(
                table: "Roles",
                keyColumn: "Id",
                keyValue: "9a51cd50-c87a-44b8-b495-f539b3e020a4");

            migrationBuilder.DeleteData(
                table: "Users",
                keyColumn: "Id",
                keyValue: new Guid("2a48f91f-4ab8-4ba7-994d-cf8ef0c7af07"));

            migrationBuilder.InsertData(
                table: "Roles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "94d6a21c-d2d3-4eb7-8efc-3d59dd7748cd", "1", "Administrator", "ADMINISTRATOR" });

            migrationBuilder.UpdateData(
                table: "UserRoles",
                keyColumn: "Id",
                keyValue: 1,
                columns: new[] { "RoleId", "UserId" },
                values: new object[] { "94d6a21c-d2d3-4eb7-8efc-3d59dd7748cd", new Guid("6555ff46-9ef0-4e59-8d23-548e1305e0c3") });

            migrationBuilder.InsertData(
                table: "Users",
                columns: new[] { "Id", "AccessFailedCount", "BirthYear", "ConcurrencyStamp", "Email", "EmailConfirmed", "LockoutEnabled", "LockoutEnd", "NormalizedEmail", "NormalizedUserName", "PasswordHash", "PasswordResetToken", "PasswordSalt", "PhoneNumber", "PhoneNumberConfirmed", "ResetTokenExpires", "SecurityStamp", "TwoFactorEnabled", "UserName", "VerificationToken", "VerifiedAt" },
                values: new object[] { new Guid("6555ff46-9ef0-4e59-8d23-548e1305e0c3"), 0, 0, "65f2b67c-6a15-4da7-a4cd-83640cbe4c8d", "admin@rustbucket.io", true, false, null, "ADMIN@RUSTBUCKET.IO", "ADMIN@RUSTBUCKET.IO", new byte[] { 65, 81, 65, 65, 65, 65, 73, 65, 65, 89, 97, 103, 65, 65, 65, 65, 69, 77, 119, 107, 84, 120, 74, 114, 114, 109, 106, 97, 100, 81, 106, 54, 87, 68, 54, 72, 67, 99, 121, 72, 107, 79, 108, 119, 103, 51, 66, 72, 99, 80, 50, 65, 114, 97, 84, 89, 84, 48, 100, 49, 74, 121, 107, 84, 86, 117, 111, 109, 57, 108, 99, 102, 113, 103, 101, 57, 55, 68, 106, 104, 104, 119, 61, 61 }, null, new byte[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }, null, false, null, "84bc1382-e780-48b1-8b90-2bc9f2f0fbd9", false, "admin@rustbucket.io", null, new DateTime(2024, 8, 2, 0, 27, 24, 687, DateTimeKind.Local).AddTicks(8902) });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(name: "UserRoles");

            migrationBuilder.DeleteData(
                table: "Roles",
                keyColumn: "Id",
                keyValue: "94d6a21c-d2d3-4eb7-8efc-3d59dd7748cd");

            migrationBuilder.DeleteData(
                table: "Users",
                keyColumn: "Id",
                keyValue: new Guid("6555ff46-9ef0-4e59-8d23-548e1305e0c3"));

            migrationBuilder.InsertData(
                table: "Roles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "9a51cd50-c87a-44b8-b495-f539b3e020a4", "1", "Administrator", "ADMINISTRATOR" });

            migrationBuilder.UpdateData(
                table: "UserRoles",
                keyColumn: "Id",
                keyValue: 1,
                columns: new[] { "RoleId", "UserId" },
                values: new object[] { "9a51cd50-c87a-44b8-b495-f539b3e020a4", new Guid("2a48f91f-4ab8-4ba7-994d-cf8ef0c7af07") });

            migrationBuilder.InsertData(
                table: "Users",
                columns: new[] { "Id", "AccessFailedCount", "BirthYear", "ConcurrencyStamp", "Email", "EmailConfirmed", "LockoutEnabled", "LockoutEnd", "NormalizedEmail", "NormalizedUserName", "PasswordHash", "PasswordResetToken", "PasswordSalt", "PhoneNumber", "PhoneNumberConfirmed", "ResetTokenExpires", "SecurityStamp", "TwoFactorEnabled", "UserName", "VerificationToken", "VerifiedAt" },
                values: new object[] { new Guid("2a48f91f-4ab8-4ba7-994d-cf8ef0c7af07"), 0, 0, "4d13e6a6-a7db-4481-a75e-beac09a28493", "admin@rustbucket.io", true, false, null, "ADMIN@RUSTBUCKET.IO", "ADMIN@RUSTBUCKET.IO", new byte[] { 65, 81, 65, 65, 65, 65, 73, 65, 65, 89, 97, 103, 65, 65, 65, 65, 69, 78, 72, 77, 88, 117, 104, 68, 115, 83, 68, 71, 119, 109, 121, 51, 97, 47, 48, 109, 56, 83, 112, 56, 111, 118, 109, 110, 122, 87, 77, 72, 103, 54, 101, 75, 117, 70, 113, 71, 86, 85, 113, 68, 85, 74, 71, 50, 81, 47, 84, 102, 57, 116, 119, 55, 49, 89, 56, 80, 119, 85, 77, 57, 105, 65, 61, 61 }, null, new byte[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }, null, false, null, "c20f0eeb-40a7-4ced-8b52-b076d2772c0d", false, "admin@rustbucket.io", null, new DateTime(2024, 8, 2, 0, 16, 22, 388, DateTimeKind.Local).AddTicks(7386) });
        }
    }
}

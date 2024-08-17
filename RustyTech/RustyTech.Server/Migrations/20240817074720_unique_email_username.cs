using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class unique_email_username : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DeleteData(
                table: "AspNetRoles",
                keyColumn: "Id",
                keyValue: "a1caeaa1-3d1e-4244-8642-4a1eacba8e7c");

            migrationBuilder.DeleteData(
                table: "AspNetUsers",
                keyColumn: "Id",
                keyValue: "f0358fab-2c3e-464e-9aeb-c5416494f4ec");

            migrationBuilder.InsertData(
                table: "AspNetRoles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "62bd08e4-de9e-4397-bcfe-a8c81e873b70", "1", "SuperAdmin", "SUPERADMINISTRATOR" });

            migrationBuilder.InsertData(
                table: "AspNetUsers",
                columns: new[] { "Id", "AccessFailedCount", "BirthYear", "ConcurrencyStamp", "Email", "EmailConfirmed", "LockoutEnabled", "LockoutEnd", "NormalizedEmail", "NormalizedUserName", "PasswordHash", "PasswordResetToken", "PasswordSalt", "PhoneNumber", "PhoneNumberConfirmed", "ResetTokenExpires", "SecurityStamp", "TwoFactorEnabled", "UserName", "VerificationToken", "VerifiedAt" },
                values: new object[] { "38f15d32-7f6f-473b-9f7c-64d3dec6fc4a", 0, 0, "b23a8ace-c560-4a0e-8560-9e195e25e645", "admin@rustbucket.io", true, false, null, "ADMIN@RUSTBUCKET.IO", "ADMIN@RUSTBUCKET.IO", new byte[] { 65, 81, 65, 65, 65, 65, 73, 65, 65, 89, 97, 103, 65, 65, 65, 65, 69, 65, 112, 77, 51, 86, 72, 97, 79, 118, 65, 87, 54, 80, 97, 90, 75, 100, 57, 74, 66, 71, 57, 68, 119, 43, 86, 76, 107, 85, 69, 105, 80, 67, 55, 49, 105, 88, 90, 120, 89, 112, 81, 114, 76, 106, 52, 115, 56, 85, 87, 66, 80, 113, 103, 83, 119, 66, 89, 78, 90, 43, 55, 47, 106, 65, 61, 61 }, null, new byte[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }, null, false, null, "b2db6d50-060f-41af-b80f-0dd0aabaebca", false, "admin@rustbucket.io", null, new DateTime(2024, 8, 17, 2, 47, 20, 396, DateTimeKind.Local).AddTicks(6517) });

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUsers_Email",
                table: "AspNetUsers",
                column: "Email",
                unique: true,
                filter: "[Email] IS NOT NULL");

            migrationBuilder.CreateIndex(
                name: "IX_AspNetUsers_UserName",
                table: "AspNetUsers",
                column: "UserName",
                unique: true,
                filter: "[UserName] IS NOT NULL");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_AspNetUsers_Email",
                table: "AspNetUsers");

            migrationBuilder.DropIndex(
                name: "IX_AspNetUsers_UserName",
                table: "AspNetUsers");

            migrationBuilder.DeleteData(
                table: "AspNetRoles",
                keyColumn: "Id",
                keyValue: "62bd08e4-de9e-4397-bcfe-a8c81e873b70");

            migrationBuilder.DeleteData(
                table: "AspNetUsers",
                keyColumn: "Id",
                keyValue: "38f15d32-7f6f-473b-9f7c-64d3dec6fc4a");

            migrationBuilder.InsertData(
                table: "AspNetRoles",
                columns: new[] { "Id", "ConcurrencyStamp", "Name", "NormalizedName" },
                values: new object[] { "a1caeaa1-3d1e-4244-8642-4a1eacba8e7c", "1", "SuperAdministrator", "SUPERADMINISTRATOR" });

            migrationBuilder.InsertData(
                table: "AspNetUsers",
                columns: new[] { "Id", "AccessFailedCount", "BirthYear", "ConcurrencyStamp", "Email", "EmailConfirmed", "LockoutEnabled", "LockoutEnd", "NormalizedEmail", "NormalizedUserName", "PasswordHash", "PasswordResetToken", "PasswordSalt", "PhoneNumber", "PhoneNumberConfirmed", "ResetTokenExpires", "SecurityStamp", "TwoFactorEnabled", "UserName", "VerificationToken", "VerifiedAt" },
                values: new object[] { "f0358fab-2c3e-464e-9aeb-c5416494f4ec", 0, 0, "bc6d5690-4938-4d6b-bca1-97987ec7e572", "admin@rustbucket.io", true, false, null, "ADMIN@RUSTBUCKET.IO", "ADMIN@RUSTBUCKET.IO", new byte[] { 65, 81, 65, 65, 65, 65, 73, 65, 65, 89, 97, 103, 65, 65, 65, 65, 69, 68, 47, 55, 79, 68, 98, 80, 112, 114, 119, 118, 109, 97, 109, 103, 85, 66, 98, 56, 43, 88, 115, 106, 100, 76, 53, 103, 67, 82, 113, 50, 109, 90, 76, 82, 79, 47, 48, 55, 84, 73, 98, 80, 120, 73, 104, 70, 70, 110, 103, 116, 51, 56, 90, 78, 72, 101, 105, 98, 99, 49, 79, 97, 71, 103, 61, 61 }, null, new byte[] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 }, null, false, null, "448517ad-92bf-423e-b1c6-457b3130157f", false, "admin@rustbucket.io", null, new DateTime(2024, 8, 15, 1, 22, 37, 473, DateTimeKind.Local).AddTicks(4425) });
        }
    }
}

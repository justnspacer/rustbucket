using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class renaming_column : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "LoginId",
                table: "Logins",
                newName: "Id");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "LoginId",
                table: "Logins",
                newName: "Id");
        }
    }
}

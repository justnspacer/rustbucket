using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class changed_logininfo_int : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "Id",
                table:"Logins",
                newName: "LoginId");

            migrationBuilder.AddColumn<int>(
                name: "Id",
                table: "Logins",
                nullable: false,
                defaultValue: 0)
                .Annotation("SqlServer:Identity", "1, 1");

            migrationBuilder.Sql("UPDATE Logins SET LoginId = NEWID()");

            migrationBuilder.DropColumn(
                name: "Id",
                table: "Logins");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<Guid>(
                name: "Id",
                table: "Logins",
                nullable: false,
                defaultValue: Guid.NewGuid());

            migrationBuilder.Sql("UPDATE LOgins SET Id = CAST(Id AS uniqueidentifier)");

            migrationBuilder.DropColumn(
                name: "Id",
                table: "Logins");

            migrationBuilder.RenameColumn(
                name: "Id",
                table: "Logins",
                newName: "LoginId");

        }
    }
}

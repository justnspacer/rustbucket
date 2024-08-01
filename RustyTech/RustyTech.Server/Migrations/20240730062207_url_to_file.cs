using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class url_to_file : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "VideoUrl",
                table: "Post",
                newName: "VideoFile");

            migrationBuilder.RenameColumn(
                name: "ImageUrls",
                table: "Post",
                newName: "ImageFiles");

            migrationBuilder.RenameColumn(
                name: "ImageUrl",
                table: "Post",
                newName: "ImageFile");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.RenameColumn(
                name: "VideoFile",
                table: "Post",
                newName: "VideoUrl");

            migrationBuilder.RenameColumn(
                name: "ImageFiles",
                table: "Post",
                newName: "ImageUrls");

            migrationBuilder.RenameColumn(
                name: "ImageFile",
                table: "Post",
                newName: "ImageUrl");
        }
    }
}

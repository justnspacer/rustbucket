using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class keyword_update : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Keywords_Post_PostId",
                table: "Keywords");

            migrationBuilder.DropIndex(
                name: "IX_Keywords_PostId",
                table: "Keywords");

            migrationBuilder.AddColumn<string>(
                name: "Keywords",
                table: "Post",
                type: "nvarchar(max)",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Keywords",
                table: "Post");

            migrationBuilder.CreateIndex(
                name: "IX_Keywords_PostId",
                table: "Keywords",
                column: "PostId");

            migrationBuilder.AddForeignKey(
                name: "FK_Keywords_Post_PostId",
                table: "Keywords",
                column: "PostId",
                principalTable: "Post",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }
    }
}

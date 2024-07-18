using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class postkeyword_refactor : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_PostKeywords_PostKeywords_PostKeywordId",
                table: "PostKeywords");

            migrationBuilder.DropIndex(
                name: "IX_PostKeywords_PostKeywordId",
                table: "PostKeywords");

            migrationBuilder.DropColumn(
                name: "PostKeywordId",
                table: "PostKeywords");

            migrationBuilder.DropColumn(
                name: "PostId",
                table: "Keywords");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "PostKeywordId",
                table: "PostKeywords",
                type: "int",
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "PostId",
                table: "Keywords",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateIndex(
                name: "IX_PostKeywords_PostKeywordId",
                table: "PostKeywords",
                column: "PostKeywordId");

            migrationBuilder.AddForeignKey(
                name: "FK_PostKeywords_PostKeywords_PostKeywordId",
                table: "PostKeywords",
                column: "PostKeywordId",
                principalTable: "PostKeywords",
                principalColumn: "Id");
        }
    }
}

using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class keyword_relationship : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Keywords_Keywords_KeywordId",
                table: "Keywords");

            migrationBuilder.DropIndex(
                name: "IX_Keywords_KeywordId",
                table: "Keywords");

            migrationBuilder.DropColumn(
                name: "Keywords",
                table: "Post");

            migrationBuilder.DropColumn(
                name: "KeywordId",
                table: "Keywords");

            migrationBuilder.CreateTable(
                name: "PostKeywords",
                columns: table => new
                {
                    PostId = table.Column<int>(type: "int", nullable: false),
                    KeywordId = table.Column<int>(type: "int", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_PostKeywords", x => new { x.PostId, x.KeywordId });
                    table.ForeignKey(
                        name: "FK_PostKeywords_Keywords_KeywordId",
                        column: x => x.KeywordId,
                        principalTable: "Keywords",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_PostKeywords_Post_PostId",
                        column: x => x.PostId,
                        principalTable: "Post",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_PostKeywords_KeywordId",
                table: "PostKeywords",
                column: "KeywordId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "PostKeywords");

            migrationBuilder.AddColumn<string>(
                name: "Keywords",
                table: "Post",
                type: "nvarchar(max)",
                nullable: true);

            migrationBuilder.AddColumn<int>(
                name: "KeywordId",
                table: "Keywords",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_Keywords_KeywordId",
                table: "Keywords",
                column: "KeywordId");

            migrationBuilder.AddForeignKey(
                name: "FK_Keywords_Keywords_KeywordId",
                table: "Keywords",
                column: "KeywordId",
                principalTable: "Keywords",
                principalColumn: "Id");
        }
    }
}

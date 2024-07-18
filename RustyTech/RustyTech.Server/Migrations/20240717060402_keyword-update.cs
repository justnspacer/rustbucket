using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RustyTech.Server.Migrations
{
    /// <inheritdoc />
    public partial class keywordupdate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "PostKeywords");

            migrationBuilder.AddColumn<string>(
                name: "Keywords",
                table: "Post",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "");

            migrationBuilder.AddColumn<Guid>(
                name: "UserId",
                table: "Keywords",
                type: "uniqueidentifier",
                nullable: false,
                defaultValue: new Guid("00000000-0000-0000-0000-000000000000"));
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Keywords",
                table: "Post");

            migrationBuilder.DropColumn(
                name: "UserId",
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
    }
}

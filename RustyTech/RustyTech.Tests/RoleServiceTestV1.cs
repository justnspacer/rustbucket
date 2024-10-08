﻿using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Logging;
using Moq;
using RustyTech.Server.Data;
using RustyTech.Server.Services;
using RustyTech.Server.Interfaces;
using RustyTech.Server.Constants;
using Microsoft.AspNetCore.Identity;
using RustyTech.Server.Models.Role;
using RustyTech.Server.Models;

namespace RustyTech.Tests
{
    public class RoleServiceTestV1
    {
        private IRoleService _roleService;
        private Mock<RoleManager<IdentityRole>> _roleManager;
        private Mock<UserManager<User>> _userManager;

        [SetUp]
        public void Setup()
        {
            var logger = new Mock<ILogger<RoleService>>();
            var userManager = new Mock<UserManager<User>>();
            var roleManager = new Mock<RoleManager<IdentityRole>>();
            _roleService = new RoleService(roleManager.Object, userManager.Object, logger.Object);
        }

        [Test]
        public async Task CreateRoleAsync_WhenRoleNameIsValid_ShouldReturnCreated()
        {
            // Arrange
            var roleName = "TestRole";

            // Act
            var result = await _roleService.CreateRole(roleName);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.Created));
        }

        [Test]
        public async Task CreateRoleAsync_WhenRoleNameIsNullOrWhiteSpace_ShouldReturnNameRequired()
        {
            // Arrange
            var roleName = "";

            // Act
            var result = await _roleService.CreateRole(roleName);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.NameRequired));
        }

        [Test]
        public async Task CreateRoleAsync_WhenRoleExists_ShouldReturnExists()
        {
            // Arrange
            var roleName = "TestRole";
            var role = new IdentityRole { Name = roleName };
            var roleManger = _roleManager.Object;
            await roleManger.CreateAsync(role);

            // Act
            var result = await _roleService.CreateRole(roleName);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.Exists));
        }

        [Test]
        public async Task GetAllRolesAsync_ShouldReturnAllRoles()
        {
            // Arrange
            var role1 = new IdentityRole { Name = "Role1", NormalizedName = "ROLE1", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var role2 = new IdentityRole { Name = "Role2", NormalizedName = "ROLE2", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var roleManger = _roleManager.Object;
            await roleManger.CreateAsync(role1);
            await roleManger.CreateAsync(role2);

            // Act
            var result = await _roleService.GetAllRoles();

            // Assert
            Assert.That(result.Count, Is.EqualTo(2));
            Assert.IsTrue(result.Any(r => r.RoleName == "Role1"));
            Assert.IsTrue(result.Any(r => r.RoleName == "Role2"));
        }

        [Test]
        public async Task GetRoleByIdAsync_WhenIdIsValid_ShouldReturnRoleDto()
        {
            // Arrange
            var role = new IdentityRole { Name = "TestRole", NormalizedName = "TESTROLE", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var roleManger = _roleManager.Object;
            await roleManger.CreateAsync(role);

            // Act
            var result = await _roleService.GetRoleById(role.Id);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Id, Is.EqualTo(role.Id));
            Assert.That(result.RoleName, Is.EqualTo(role.Name));
        }

        [Test]
        public async Task GetRoleByIdAsync_WhenIdIsNullOrEmpty_ShouldReturnNull()
        {
            // Arrange
            string id = string.Empty;

            // Act
            var result = await _roleService.GetRoleById(id);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task GetRoleByNameAsync_WhenRoleNameIsValid_ShouldReturnRoleDto()
        {
            // Arrange
            var role = new IdentityRole { Name = "TestRole", NormalizedName = "TESTROLE", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var roleManger = _roleManager.Object;
            await roleManger.CreateAsync(role);

            // Act
            var result = await _roleService.GetRoleByName(role.Name);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Id, Is.EqualTo(role.Id));
            Assert.That(result.RoleName, Is.EqualTo(role.Name));
        }

        [Test]
        public async Task GetRoleByNameAsync_WhenRoleNameIsNullOrEmpty_ShouldReturnNull()
        {
            // Arrange
            string roleName = null;

            // Act
            var result = await _roleService.GetRoleByName(roleName);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task GetUserRolesAsync_WhenIdIsValid_ShouldReturnUserRoles()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var role1 = new IdentityRole { Name = "Role1", NormalizedName = "ROLE1", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var role2 = new IdentityRole { Name = "Role2", NormalizedName = "ROLE2", ConcurrencyStamp = Guid.NewGuid().ToString() };
            var roleManger = _roleManager.Object;
            var userManager = _userManager.Object;
            await roleManger.CreateAsync(role1);
            await roleManger.CreateAsync(role2);
            await userManager.AddToRoleAsync(user, role1.Name);
            await userManager.AddToRoleAsync(user, role2.Name);

            // Act
            var result = await _roleService.GetUserRoles(user.Id);

            // Assert
            Assert.IsNotNull(result);
            Assert.That(result.Count, Is.EqualTo(2));
            Assert.IsTrue(result.Any(name => name == role1.Name));
            Assert.IsTrue(result.Any(name => name == role2.Name));
        }

        [Test]
        public async Task GetUserRolesAsync_WhenIdIsEmpty_ShouldReturnNull()
        {
            // Arrange
            string id = string.Empty;

            // Act
            var result = await _roleService.GetUserRoles(id);

            // Assert
            Assert.IsNull(result);
        }

        [Test]
        public async Task AddRoleToUserAsync_WhenRequestIsValid_ShouldReturnAddedToUser()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var role = new IdentityRole { Name = "TestRole" };
            var roleManger = _roleManager.Object;
            var userManager = _userManager.Object;
            await roleManger.CreateAsync(role);
            await userManager.CreateAsync(user);

            var request = new RoleRequest { RoleId = "1", RoleName = role.Name, UserId = user.Id };

            // Act
            var result = await _roleService.AddRoleToUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.AddedToUser));
        }

        [Test]
        public async Task AddRoleToUserAsync_WhenRoleNameIsNullOrWhiteSpace_ShouldReturnBadRequest()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var request = new RoleRequest { RoleId = "1",  RoleName = "", UserId = user.Id };

            // Act
            var result = await _roleService.AddRoleToUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Error.BadRequest));
        }

        [Test]
        public async Task AddRoleToUserAsync_WhenUserIdIsEmpty_ShouldReturnBadRequest()
        {
            // Arrange
            var request = new RoleRequest { RoleId = "1", RoleName = "TestRole", UserId = string.Empty };

            // Act
            var result = await _roleService.AddRoleToUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Error.BadRequest));
        }

        [Test]
        public async Task AddRoleToUserAsync_WhenUserNotFound_ShouldReturnUserNotFound()
        {
            // Arrange
            var request = new RoleRequest { RoleId = "1", RoleName = "TestRole", UserId = Guid.NewGuid().ToString() };

            // Act
            var result = await _roleService.AddRoleToUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Info.UserNotFound));
        }

        [Test]
        public async Task AddRoleToUserAsync_WhenRoleNotFound_ShouldReturnNotFound()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var userManager = _userManager.Object;
            await userManager.CreateAsync(user);

            var request = new RoleRequest { RoleId = "1", RoleName = "TestRole", UserId = user.Id };

            // Act
            var result = await _roleService.AddRoleToUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.NotFound));
        }

        [Test]
        public async Task RemoveRoleFromUserAsync_WhenRequestIsValid_ShouldReturnRemoved()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var role = new IdentityRole { Name = "TestRole" };
            var roleManger = _roleManager.Object;
            var userManager = _userManager.Object;
            await roleManger.CreateAsync(role);
            await userManager.CreateAsync(user);

            await userManager.AddToRoleAsync(user, role.Name);
            var request = new RoleRequest { RoleName = "TestRole", RoleId = role.Id, UserId = user.Id };

            // Act
            var result = await _roleService.RemoveRoleFromUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Role.Removed));
        }

        [Test]
        public async Task RemoveRoleFromUserAsync_WhenRoleIdIsNullOrWhiteSpace_ShouldReturnBadRequest()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var request = new RoleRequest { RoleName = string.Empty, RoleId = string.Empty, UserId = user.Id };

            // Act
            var result = await _roleService.RemoveRoleFromUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Error.BadRequest));
        }

        [Test]
        public async Task RemoveRoleFromUserAsync_WhenUserIdIsEmpty_ShouldReturnBadRequest()
        {
            // Arrange
            var request = new RoleRequest { RoleName = string.Empty, RoleId = "TestRoleId", UserId = string.Empty };

            // Act
            var result = await _roleService.RemoveRoleFromUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Error.BadRequest));
        }

        [Test]
        public async Task RemoveRoleFromUserAsync_WhenUserNotFound_ShouldReturnUserNotFound()
        {
            // Arrange
            var request = new RoleRequest { RoleName = string.Empty, RoleId = "TestRoleId", UserId = Guid.NewGuid().ToString() };

            // Act
            var result = await _roleService.RemoveRoleFromUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Info.UserNotFound));
        }

        [Test]
        public async Task RemoveRoleFromUserAsync_WhenUserRoleNotFound_ShouldReturnNotFound()
        {
            // Arrange
            var user = new User { Id = Guid.NewGuid().ToString() };
            var userManager = _userManager.Object;
            await userManager.CreateAsync(user);

            var request = new RoleRequest { RoleName = string.Empty, RoleId = "TestRoleId", UserId = user.Id };

            // Act
            var result = await _roleService.RemoveRoleFromUser(request);

            // Assert
            Assert.That(result.Message, Is.EqualTo(Messages.Info.UserNotFound));
        }
    }
}

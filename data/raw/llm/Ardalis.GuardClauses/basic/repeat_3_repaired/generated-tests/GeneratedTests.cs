using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Runtime.CompilerServices;
using Ardalis.GuardClauses;

namespace Ardalis.GuardClauses.Tests
{
    public static class GuardClauseExtensionsTests
    {
        [Fact]
        public static void Null_ThrowsArgumentNullException_WhenInputIsNull()
        {
            // Arrange
            var guardClause = new GuardClauseExtensions();
            var input = null;

            // Act
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null(input, nameof(input)));

            // Assert
            Assert.Equal(nameof(input), exception.ParamName);
            Assert.Equal("input is null", exception.Message);
        }

        [Fact]
        public static void Null_ThrowsArgumentException_WhenInputIsEmptyString()
        {
            // Arrange
            var guardClause = new GuardClauseExtensions();
            var input = string.Empty;

            // Act
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null(input, nameof(input)));

            // Assert
            Assert.Equal(nameof(input), exception.ParamName);
            Assert.Equal("input is empty", exception.Message);
        }

        [Fact]
        public static void Null_ThrowsArgumentException_WhenInputIsEmptyGuid()
        {
            // Arrange
            var guardClause = new GuardClauseExtensions();
            var input = Guid.Empty;

            // Act
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null(input, nameof(input)));

            // Assert
            Assert.Equal(nameof(input), exception.ParamName);
            Assert.Equal("input is empty", exception.Message);
        }
    }
}
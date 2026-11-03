using System;
using Ardalis.GuardClauses;
using Xunit;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void NullGuard()
        {
            // Test with null value
            var guard = Guard.Against.Null(null, nameof(nullValue));
            Assert.Throws<ArgumentNullException>(guard);

            // Test with non-null value
            var guard2 = Guard.Against.Null("Test", nameof(testValue));
            Assert.True(guard2);
        }

        [Fact]
        public void NullOrEmptyGuard()
        {
            // Test with empty string
            var guard = Guard.Against.NullOrEmpty(string.Empty, nameof(emptyString));
            Assert.True(guard);

            // Test with non-empty string
            var guard2 = Guard.Against.NullOrEmpty("Test", nameof(testString));
            Assert.True(guard2);
        }

        [Fact]
        public void NullOrEmptyGuidGuard()
        {
            // Test with valid GUID
            var guard = Guard.Against.NullOrEmpty(Guid.NewGuid(), nameof(guidValue));
            Assert.True(guard);

            // Test with invalid GUID (e.g., empty string)
            var guard2 = Guard.Against.NullOrEmpty(Guid.Empty, nameof(invalidGuid));
            Assert.False(guard2);
        }

        [Fact]
        public void NullOrWhiteSpaceGuard()
        {
            // Test with whitespace string
            var guard = Guard.Against.NullOrWhiteSpace("  ", nameof(whitespaceString));
            Assert.True(guard);

            // Test with non-whitespace string
            var guard2 = Guard.Against.NullOrWhiteSpace("Test", nameof(testString));
            Assert.True(guard2);
        }

        [Fact]
        public void DefaultGuard()
        {
            // Test with default value
            var guard = Guard.Against.Default(Guid.Empty, nameof(defaultGuid));
            Assert.True(guard);

            // Test with non-default value
            var guard2 = Guard.Against.Default("Test", nameof(defaultString));
            Assert.True(guard2);
        }

        [Fact]
        public void NullOrInvalidInputGuard()
        {
            // Test with valid input
            var guard = Guard.Against.NullOrInvalidInput(123, nameof(validInput), null);
            Assert.True(guard);

            // Test with invalid input (e.g., null)
            var guard2 = Guard.Against.NullOrInvalidInput(null, nameof(invalidInput), null);
            Assert.False(guard2);
        }
    }
}
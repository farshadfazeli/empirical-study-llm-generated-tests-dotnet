using System;
using Ardalis.GuardClauses;
using Xunit;

namespace GuardTests
    public class GuardTests
        [Fact]
        public void Null_WhenInputIsNull()
            var guard = new GuardClauseExtensions();
            var result = guard.Null(null, nameof(null), "Input cannot be null.");
            Assert.IsType<ArgumentNullException>(result);

        [Fact]
        public void Null_WhenInputIsInvalid()
            var guard = new GuardClauseExtensions();
            var result = guard.Null(new object(), nameof(object), "Input is invalid.");
            Assert.IsType<ArgumentException>(result);

        [Fact]
        public void Null_WhenInputIsInvalidAndExceptionCreatorIsProvided()
            var guard = new GuardClauseExtensions();
            var result = guard.Null(new object(), nameof(object), "Input is invalid.", () => new ArgumentException("Invalid input."));
            Assert.IsType<ArgumentException>(result);
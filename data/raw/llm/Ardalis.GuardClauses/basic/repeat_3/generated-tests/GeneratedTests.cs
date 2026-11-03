using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

namespace Ardalis.GuardClauses.Tests
{
    public class GuardClauseExtensionsTests
    {
        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", null));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentException_WhenInputIsNullAndMessageIsProvided()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null<object>(null, "input", "message", null));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName")));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName")));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvided()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), "message"));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvided()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), "message"));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), () => new ArgumentNullException("parameterName", "message")));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), () => new ArgumentNullException("parameterName", "message")));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvided()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), () => new ArgumentNullException("parameterName", "message"), "message"));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvided()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), () => new ArgumentNullException("parameterName", "message"), "message"));
            Assert.NotNull(exception);
        }

        [Fact]
        public void Null_ThrowsArgumentNullException_WhenInputIsNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNullAndMessageIsProvidedAndExceptionCreatorIsNotNull()
        {
            var guardClause = new GuardClauseExtensions();
            var exception = Assert.Throws<ArgumentNullException>(() => guardClause.Null<object>(null, "input", "message", () => new ArgumentNullException("parameterName"), () => new ArgumentNullException("parameterName", "message"), () => new ArgumentNullException("parameterName", "message
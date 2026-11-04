using System;
using Ardalis.GuardClauses;
using Xunit;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void Null_returns_the_original_value_when_input_is_not_null()
        {
            var value = "value";
            var result = Guard.Against.Null(value, nameof(value));
            Assert.Same(value, result);
        }
    }
}
using System;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void Null_returns_the_original_value_when_input_is_not_null()
        {
            var value = null;
            var result = Guard.Against.Null(value, "value cannot be null");
            Assert.Equal(value, result);
        }
    }
}
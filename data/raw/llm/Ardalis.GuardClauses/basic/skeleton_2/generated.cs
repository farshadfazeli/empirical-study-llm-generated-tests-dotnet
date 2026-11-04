using System;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void Null_returns_the_original_value_when_input_is_not_null()
        {
            var originalValue = "Original Value";
            var result = Guard.Against.Null(originalValue, "Input cannot be null");

            Assert.Equal(originalValue, result);
        }
    }
}
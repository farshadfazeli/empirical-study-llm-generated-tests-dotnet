using System;
using Ardalis.GuardClauses;
using Xunit;

namespace Ardalis.GuardClauses.HumanTests;

public class GuardAgainstNullHumanTests
{
    [Fact]
    public void Null_returns_the_original_value_when_input_is_not_null()
    {
        var input = "value";

        var result = Guard.Against.Null(input);

        Assert.Same(input, result);
    }

    [Fact]
    public void Null_throws_argument_null_exception_for_null_input()
    {
        string? input = null;

        var exception = Assert.Throws<ArgumentNullException>(() => Guard.Against.Null(input, nameof(input)));

        Assert.Equal(nameof(input), exception.ParamName);
    }

    [Fact]
    public void Null_uses_a_custom_message_when_one_is_supplied()
    {
        string? input = null;

        var exception = Assert.Throws<ArgumentNullException>(() => Guard.Against.Null(input, nameof(input), "custom message"));

        Assert.StartsWith("custom message", exception.Message, StringComparison.Ordinal);
    }
}

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

namespace Ardalis.GuardClauses
{
    /// <summary>
    /// A collection of common guard clauses, implemented as extensions.
    /// </summary>
    /// <example>
    /// Guard.Against.Null(input, nameof(input));
    /// </example>
    public static partial class GuardClauseExtensions
    {
        /// <summary>
        /// Throws an <see cref="ArgumentNullException" /> or a custom <see cref="Exception" /> if <paramref name="input" /> is null.
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="guardClause"></param>
        /// <param name="input"></param>
        /// <param name="parameterName"></param>
        /// <param name="message">Optional. Custom error message</param>
        /// <param name="exceptionCreator"></param>
        /// <returns><paramref name="input" /> if the value is not null.</returns>
        /// <exception cref="Exception"></exception>
        public static T Null<T>(this IGuardClause guardClause,
            [NotNull][ValidatedNotNull]T? input,
            [CallerArgumentExpression("input")] string? parameterName = null,
            string? message = null,
            Func<Exception>? exceptionCreator = null)
        {
            if (input is null)
            {
                Exception? exception = exceptionCreator?.Invoke();

                if (string.IsNullOrEmpty(message))
                {
                    throw exception ?? new ArgumentNullException(parameterName);
                }
                throw exception ?? new ArgumentNullException(parameterName, message);
            }

            return input;
        }

        /// <summary>
        /// Throws an <see cref="ArgumentNullException" /> or a custom <see cref="Exception" /> if <paramref name="input" /> is null.
        /// Throws an <see cref="ArgumentException" /> or a custom <see cref="Exception" /> if <paramref name="input" /> is an empty string.
        /// </summary>
        /// <param name="guardClause"></param>
        /// <param name="input"></param>
        /// <param name="parameterName"></param>
        /// <param name="message">Optional. Custom error message</param>
        /// <param name="exceptionCreator"></param>
        /// <returns><paramref name="input" /> if the value is not an empty string or null.</returns>
        /// <exception cref="ArgumentNullException"></exception>
        /// <exception cref="ArgumentException"></exception>
        /// <exception cref="Exception"></exception>
        public static string NullOrEmpty(this IGuardClause guardClause,
            [NotNull][ValidatedNotNull] string? input,
            [CallerArgumentExpression("input")] string? parameterName = null,
            string? message = null,
            Func<Exception>? exceptionCreator = null)
        {
            Guard.Against.Null(input, parameterName, message, exceptionCreator);
            if (input == string.Empty)
            {
                throw exceptionCreator?.Invoke() ?? 
                    new ArgumentException(message ?? $"Required input {parameterName} was empty.", parameterName);
            }

            return input;
        }

        /// <summary>
        /// Throws an <see cref="ArgumentNullException" /> or a custom <see cref="Exception" />if <paramref name="input" /> is null.
        /// Throws an <see cref="
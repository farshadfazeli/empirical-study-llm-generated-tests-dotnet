using System;
using System.Collections.Generic;
using System.Diagnostics.CodeAnalysis;
using System.Linq;
using System.Runtime.CompilerServices;

namespace Ardalis.GuardClauses.Tests

    /// <summary>
    /// A collection of common guard clauses, implemented as extensions.
    /// </summary>
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
        /// </summary>
        /// <typeparam name="T">Must be a value type.</typeparam>
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
            Func<Exception>? exceptionCreator = null) where T : struct
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

            return input.Value;
        }

        /// <summary>
        /// Throws an <see cref="ArgumentNullException" /> or a custom <see cref="Exception" /> if <paramref name="input" /> is null.
        /// Throws an <see cref="ArgumentException" /> or a custom <see cref="Exception" /> if <paramref name="input" /> is an empty string.
        /// </summary>
        /// <param name="guardClause"></param>
        /// <param name="input"></param>
        /// <param
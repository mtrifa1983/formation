package calculator;

/**
 * Simple calculator with basic arithmetic operations.
 *
 * Examples:
 * <pre>
 * Calculator.add(2, 3); // returns 5.0
 * Calculator.sub(5, 1); // returns 4.0
 * Calculator.mul(3, 4); // returns 12.0
 * Calculator.div(10, 2); // returns 5.0
 * </pre>
 */
public class Calculator {

    /**
     * Add two numbers.
     *
     * @param a first operand
     * @param b second operand
     * @return sum as double
     */
    public static double add(double a, double b) {
        return a + b;
    }

    /**
     * Subtract two numbers (a - b).
     *
     * @param a first operand
     * @param b second operand
     * @return difference as double
     */
    public static double sub(double a, double b) {
        return a - b;
    }

    /**
     * Multiply two numbers.
     *
     * @param a first operand
     * @param b second operand
     * @return product as double
     */
    public static double mul(double a, double b) {
        return a * b;
    }

    /**
     * Divide two numbers (a / b). Throws ArithmeticException on division by zero.
     *
     * @param a numerator
     * @param b denominator
     * @return quotient as double
     * @throws ArithmeticException when dividing by zero
     */
    public static double div(double a, double b) throws ArithmeticException {
        if (b == 0.0) {
            throw new ArithmeticException("Division by zero");
        }
        return a / b;
    }
}

package calculator;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the Calculator class.
 * Tests all basic arithmetic operations and edge cases.
 */
@DisplayName("Calculator Tests")
public class CalculatorTest {

    @Test
    @DisplayName("should add two positive numbers")
    void testAddPositive() {
        double result = Calculator.add(2, 3);
        assertEquals(5.0, result, "2 + 3 should equal 5.0");
    }

    @Test
    @DisplayName("should add two negative numbers")
    void testAddNegative() {
        double result = Calculator.add(-2, -3);
        assertEquals(-5.0, result, "-2 + -3 should equal -5.0");
    }

    @Test
    @DisplayName("should add positive and negative numbers")
    void testAddMixed() {
        double result = Calculator.add(10, -3);
        assertEquals(7.0, result, "10 + -3 should equal 7.0");
    }

    @Test
    @DisplayName("should add zero")
    void testAddZero() {
        double result = Calculator.add(0, 5);
        assertEquals(5.0, result, "0 + 5 should equal 5.0");
    }

    @Test
    @DisplayName("should subtract two positive numbers")
    void testSubPositive() {
        double result = Calculator.sub(10, 3);
        assertEquals(7.0, result, "10 - 3 should equal 7.0");
    }

    @Test
    @DisplayName("should subtract two negative numbers")
    void testSubNegative() {
        double result = Calculator.sub(-2, -3);
        assertEquals(1.0, result, "-2 - -3 should equal 1.0");
    }

    @Test
    @DisplayName("should subtract positive and negative numbers")
    void testSubMixed() {
        double result = Calculator.sub(5, -3);
        assertEquals(8.0, result, "5 - -3 should equal 8.0");
    }

    @Test
    @DisplayName("should subtract zero")
    void testSubZero() {
        double result = Calculator.sub(5, 0);
        assertEquals(5.0, result, "5 - 0 should equal 5.0");
    }

    @Test
    @DisplayName("should multiply two positive numbers")
    void testMulPositive() {
        double result = Calculator.mul(4, 5);
        assertEquals(20.0, result, "4 * 5 should equal 20.0");
    }

    @Test
    @DisplayName("should multiply two negative numbers")
    void testMulNegative() {
        double result = Calculator.mul(-4, -5);
        assertEquals(20.0, result, "-4 * -5 should equal 20.0");
    }

    @Test
    @DisplayName("should multiply positive and negative numbers")
    void testMulMixed() {
        double result = Calculator.mul(4, -5);
        assertEquals(-20.0, result, "4 * -5 should equal -20.0");
    }

    @Test
    @DisplayName("should multiply by zero")
    void testMulZero() {
        double result = Calculator.mul(5, 0);
        assertEquals(0.0, result, "5 * 0 should equal 0.0");
    }

    @Test
    @DisplayName("should divide two positive numbers")
    void testDivPositive() {
        double result = Calculator.div(10, 2);
        assertEquals(5.0, result, "10 / 2 should equal 5.0");
    }

    @Test
    @DisplayName("should divide two negative numbers")
    void testDivNegative() {
        double result = Calculator.div(-10, -2);
        assertEquals(5.0, result, "-10 / -2 should equal 5.0");
    }

    @Test
    @DisplayName("should divide positive and negative numbers")
    void testDivMixed() {
        double result = Calculator.div(10, -2);
        assertEquals(-5.0, result, "10 / -2 should equal -5.0");
    }

    @Test
    @DisplayName("should divide by zero throws ArithmeticException")
    void testDivByZero() {
        assertThrows(ArithmeticException.class, () -> Calculator.div(5, 0),
            "Dividing by zero should throw ArithmeticException");
    }

    @Test
    @DisplayName("should handle decimal division")
    void testDivDecimal() {
        double result = Calculator.div(5, 2);
        assertEquals(2.5, result, 0.0001, "5 / 2 should equal 2.5");
    }
}

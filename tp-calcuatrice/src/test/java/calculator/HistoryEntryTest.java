package calculator;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the HistoryEntry class.
 * Tests creation and properties of history entries.
 */
@DisplayName("HistoryEntry Tests")
public class HistoryEntryTest {

    @Test
    @DisplayName("should create a history entry with correct values")
    void testCreateEntry() {
        HistoryEntry entry = new HistoryEntry("add", 5, 3, 8.0);
        
        assertEquals("add", entry.op, "Operation should be 'add'");
        assertEquals(5, entry.a, "First operand should be 5");
        assertEquals(3, entry.b, "Second operand should be 3");
        assertEquals(8.0, entry.result, "Result should be 8.0");
    }

    @Test
    @DisplayName("should automatically generate timestamp")
    void testTimestampGeneration() {
        HistoryEntry entry = new HistoryEntry("sub", 10, 2, 8.0);
        
        assertNotNull(entry.when, "Timestamp should not be null");
        assertFalse(entry.when.isEmpty(), "Timestamp should not be empty");
    }

    @Test
    @DisplayName("should have ISO-8601 format timestamp")
    void testTimestampFormat() {
        HistoryEntry entry = new HistoryEntry("mul", 4, 5, 20.0);
        
        // ISO-8601 format contains 'T' between date and time
        assertTrue(entry.when.contains("T"), "Timestamp should be in ISO-8601 format");
    }

    @Test
    @DisplayName("should handle negative operands")
    void testNegativeOperands() {
        HistoryEntry entry = new HistoryEntry("add", -5, -3, -8.0);
        
        assertEquals(-5, entry.a, "First operand should be -5");
        assertEquals(-3, entry.b, "Second operand should be -3");
        assertEquals(-8.0, entry.result, "Result should be -8.0");
    }

    @Test
    @DisplayName("should handle decimal results")
    void testDecimalResults() {
        HistoryEntry entry = new HistoryEntry("div", 5, 2, 2.5);
        
        assertEquals(2.5, entry.result, "Result should be 2.5");
    }

    @Test
    @DisplayName("should handle all operation types")
    void testDifferentOperations() {
        HistoryEntry add = new HistoryEntry("add", 1, 2, 3.0);
        HistoryEntry sub = new HistoryEntry("sub", 5, 2, 3.0);
        HistoryEntry mul = new HistoryEntry("mul", 3, 4, 12.0);
        HistoryEntry div = new HistoryEntry("div", 10, 2, 5.0);
        
        assertEquals("add", add.op, "Operation should be 'add'");
        assertEquals("sub", sub.op, "Operation should be 'sub'");
        assertEquals("mul", mul.op, "Operation should be 'mul'");
        assertEquals("div", div.op, "Operation should be 'div'");
    }
}

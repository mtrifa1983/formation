package calculator;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.io.IOException;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Unit tests for the HistoryManager class.
 * Tests loading, saving, and managing operation history.
 */
@DisplayName("HistoryManager Tests")
public class HistoryManagerTest {

    private HistoryManager historyManager;
    private List<HistoryEntry> testEntries;

    @BeforeEach
    void setUp(@TempDir Path tempDir) {
        // Use a temporary directory for each test to avoid file conflicts
        String historyPath = tempDir.resolve("test_history.json").toString();
        historyManager = new HistoryManager(historyPath);
        testEntries = new ArrayList<>();
    }

    @Test
    @DisplayName("should save a list of history entries to file")
    void testSaveEntries() throws IOException {
        testEntries.add(new HistoryEntry("add", 2, 3, 5.0));
        
        historyManager.save(testEntries);
        List<HistoryEntry> loaded = historyManager.load();
        
        assertEquals(1, loaded.size(), "Should have 1 entry after save");
        assertEquals("add", loaded.get(0).op, "Operation should be 'add'");
        assertEquals(2, loaded.get(0).a, "First operand should be 2");
        assertEquals(3, loaded.get(0).b, "Second operand should be 3");
        assertEquals(5.0, loaded.get(0).result, "Result should be 5.0");
    }

    @Test
    @DisplayName("should save multiple entries")
    void testSaveMultipleEntries() throws IOException {
        testEntries.add(new HistoryEntry("add", 2, 3, 5.0));
        testEntries.add(new HistoryEntry("sub", 10, 4, 6.0));
        testEntries.add(new HistoryEntry("mul", 3, 4, 12.0));
        
        historyManager.save(testEntries);
        List<HistoryEntry> loaded = historyManager.load();
        
        assertEquals(3, loaded.size(), "Should have 3 entries after save");
    }

    @Test
    @DisplayName("should persist history to file and load later")
    void testPersistHistory(@TempDir Path tempDir) throws IOException {
        String historyPath = tempDir.resolve("persist_test.json").toString();
        HistoryManager manager1 = new HistoryManager(historyPath);
        
        List<HistoryEntry> entries = new ArrayList<>();
        entries.add(new HistoryEntry("add", 5, 3, 8.0));
        manager1.save(entries);
        
        // Create a new manager pointing to the same file
        HistoryManager manager2 = new HistoryManager(historyPath);
        List<HistoryEntry> loaded = manager2.load();
        
        assertEquals(1, loaded.size(), "Loaded history should contain 1 entry");
        assertEquals("add", loaded.get(0).op, "Loaded operation should be 'add'");
    }

    @Test
    @DisplayName("should handle empty history")
    void testEmptyHistory() throws IOException {
        List<HistoryEntry> loaded = historyManager.load();
        assertEquals(0, loaded.size(), "Empty file should load as empty list");
    }

    @Test
    @DisplayName("should handle division operations in history")
    void testDivisionHistory() throws IOException {
        testEntries.add(new HistoryEntry("div", 10, 2, 5.0));
        
        historyManager.save(testEntries);
        List<HistoryEntry> loaded = historyManager.load();
        
        assertEquals(1, loaded.size(), "Should have 1 entry");
        assertEquals("div", loaded.get(0).op, "Operation should be 'div'");
        assertEquals(5.0, loaded.get(0).result, "Result should be 5.0");
    }

    @Test
    @DisplayName("should have timestamp for each entry")
    void testEntryHasTimestamp() {
        HistoryEntry entry = new HistoryEntry("add", 2, 3, 5.0);
        assertNotNull(entry.when, "Entry should have a timestamp");
        assertFalse(entry.when.isEmpty(), "Timestamp should not be empty");
    }

    @Test
    @DisplayName("should load non-existent file as empty list")
    void testLoadNonExistentFile() throws IOException {
        HistoryManager manager = new HistoryManager("/path/that/does/not/exist/history.json");
        List<HistoryEntry> loaded = manager.load();
        
        assertEquals(0, loaded.size(), "Non-existent file should load as empty list");
    }

    @Test
    @DisplayName("should handle negative operands")
    void testNegativeOperands() throws IOException {
        testEntries.add(new HistoryEntry("add", -5, -3, -8.0));
        
        historyManager.save(testEntries);
        List<HistoryEntry> loaded = historyManager.load();
        
        assertEquals(-5, loaded.get(0).a, "First operand should be -5");
        assertEquals(-3, loaded.get(0).b, "Second operand should be -3");
    }
}


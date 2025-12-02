package calculator;

import java.time.Instant;

/**
 * A record of one calculation.
 */
public class HistoryEntry {
    public String op;
    public double a;
    public double b;
    public double result;
    public String when; // ISO-8601 string

    public HistoryEntry(String op, double a, double b, double result) {
        this.op = op;
        this.a = a;
        this.b = b;
        this.result = result;
        this.when = Instant.now().toString();
    }
}

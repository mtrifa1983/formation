package calculator;

import java.util.*;
import java.io.IOException;

/**
 * CLI entrypoint for the calculator.
 *
 * Usage examples:
 * java -cp target/classes;target/dependency/* calculator.Main
 * java -cp target/classes;target/dependency/* calculator.Main add 2 3
 * java -cp target/classes;target/dependency/* calculator.Main --history history.json
 *
 * Interactive commands:
 *  - add <a> <b>
 *  - sub <a> <b>
 *  - mul <a> <b>
 *  - div <a> <b>
 *  - history  (show history file entries)
 *  - save     (save current history)
 *  - quit
 */
public class Main {
    public static void main(String[] args) {
        String historyPath = "history.json";
        List<String> argList = new ArrayList<>(Arrays.asList(args));
        // simple arg parsing for --history <path>
        for (int i = 0; i < argList.size(); i++) {
            if ("--history".equals(argList.get(i)) && i + 1 < argList.size()) {
                historyPath = argList.get(i + 1);
                // remove both args
                argList.remove(i + 1);
                argList.remove(i);
                break;
            }
        }

        HistoryManager hm = new HistoryManager(historyPath);
        List<HistoryEntry> history = new ArrayList<>();
        try {
            history = hm.load();
        } catch (IOException e) {
            // ignore, start with empty history
        }

        if (argList.size() >= 1) {
            // non-interactive mode: first arg is operation
            String op = argList.get(0);
            if (argList.size() < 3) {
                System.err.println("Usage: <op> <a> <b>\nops: add sub mul div");
                System.exit(2);
            }
            try {
                double a = Double.parseDouble(argList.get(1));
                double b = Double.parseDouble(argList.get(2));
                double res = perform(op, a, b, history, hm);
                System.out.println(res);
            } catch (NumberFormatException ex) {
                System.err.println("Invalid number");
                System.exit(2);
            } catch (ArithmeticException ex) {
                System.err.println("Error: " + ex.getMessage());
                System.exit(3);
            } catch (IOException ex) {
                System.err.println("I/O error saving history: " + ex.getMessage());
                System.exit(4);
            }
            return;
        }

        // interactive mode
        Scanner sc = new Scanner(System.in);
        System.out.println("Calculator CLI — type 'help' for commands");
        while (true) {
            System.out.print("calc> ");
            String line = sc.nextLine();
            if (line == null) break;
            line = line.trim();
            if (line.isEmpty()) continue;
            String[] parts = line.split("\\s+");
            String cmd = parts[0].toLowerCase();
            try {
                switch (cmd) {
                    case "quit":
                    case "exit":
                        System.out.println("Bye");
                        return;
                    case "help":
                        System.out.println("Commands: add/sub/mul/div a b | history | save | quit");
                        break;
                    case "history":
                        for (HistoryEntry e : history) {
                            System.out.printf("%s %s %s = %s @ %s\n", e.op, e.a, e.b, e.result, e.when);
                        }
                        break;
                    case "save":
                        hm.save(history);
                        System.out.println("Saved history to " + historyPath);
                        break;
                    case "add":
                    case "sub":
                    case "mul":
                    case "div":
                        if (parts.length < 3) { System.out.println("Usage: " + cmd + " a b"); break; }
                        double a = Double.parseDouble(parts[1]);
                        double b = Double.parseDouble(parts[2]);
                        double r = perform(cmd, a, b, history, hm);
                        System.out.println("= " + r);
                        break;
                    default:
                        System.out.println("Unknown command. Type help.");
                }
            } catch (NumberFormatException ex) {
                System.out.println("Invalid number");
            } catch (ArithmeticException ex) {
                System.out.println("Error: " + ex.getMessage());
            } catch (IOException ex) {
                System.out.println("I/O error: " + ex.getMessage());
            }
        }
    }

    private static double perform(String op, double a, double b, List<HistoryEntry> history, HistoryManager hm) throws IOException {
        double r;
        switch (op) {
            case "add": r = Calculator.add(a, b); break;
            case "sub": r = Calculator.sub(a, b); break;
            case "mul": r = Calculator.mul(a, b); break;
            case "div": r = Calculator.div(a, b); break;
            default: throw new IllegalArgumentException("Unknown op: " + op);
        }
        HistoryEntry e = new HistoryEntry(op, a, b, r);
        history.add(e);
        hm.save(history);
        return r;
    }
}

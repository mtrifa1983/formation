import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

public class DateFunction {
    
    /**
     * Returns today's date as a string in format yyyy-MM-dd
     * @return today's date
     */
    public static String getTodayDate() {
        return LocalDate.now().toString();
    }
    
    /**
     * Returns today's date in a custom format
     * @param pattern the date format pattern (e.g., "dd/MM/yyyy")
     * @return today's date formatted according to the pattern
     */
    public static String getTodayDate(String pattern) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern(pattern);
        return LocalDate.now().format(formatter);
    }
    
    /**
     * Returns today's date as a LocalDate object
     * @return today's date as LocalDate
     */
    public static LocalDate getTodayAsLocalDate() {
        return LocalDate.now();
    }
    
    // Example usage
    public static void main(String[] args) {
        System.out.println("Today's date: " + getTodayDate());
        System.out.println("Today's date (dd/MM/yyyy): " + getTodayDate("dd/MM/yyyy"));
        System.out.println("Today's date (EEEE, dd MMMM yyyy): " + getTodayDate("EEEE, dd MMMM yyyy"));
    }
}



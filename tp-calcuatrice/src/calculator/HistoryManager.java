package calculator;

import java.io.FileWriter;
import java.io.IOException;
import java.io.FileReader;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.lang.reflect.Type;

/**
 * Simple JSON history manager using Gson.
 */
public class HistoryManager {
    private final File file;
    private final Gson gson = new Gson();

    public HistoryManager(String path) {
        this.file = new File(path);
    }

    public void save(List<HistoryEntry> entries) throws IOException {
        try (FileWriter fw = new FileWriter(file)) {
            gson.toJson(entries, fw);
        }
    }

    public List<HistoryEntry> load() throws IOException {
        if (!file.exists()) {
            return new ArrayList<>();
        }
        try (FileReader fr = new FileReader(file)) {
            Type t = new TypeToken<List<HistoryEntry>>() {}.getType();
            List<HistoryEntry> list = gson.fromJson(fr, t);
            return list != null ? list : new ArrayList<>();
        }
    }
}

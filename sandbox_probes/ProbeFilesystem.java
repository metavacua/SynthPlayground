import java.io.*;
import java.nio.file.*;

/**
 * Filesystem Probe - Phase 1
 *
 * Goal: Determine what filesystem access the agent actually has through
 * concrete experimentation (read, write, list operations) on various paths.
 *
 * Design Philosophy:
 * - Each test returns specific diagnostic information (exception type + message)
 * - Output is structured for both human reading and machine parsing
 * - Tests are designed to prove/refute specific capabilities
 */
public class ProbeFilesystem {
    public static void main(String[] args) throws Exception {
        System.out.println("=== FILESYSTEM PROBE START ===");
        System.out.println("Timestamp: " + java.time.Instant.now().toString());
        System.out.println();

        // Test 1: Can we read /etc/hostname?
        testRead("/etc/hostname");

        // Test 2: Can we write to /workspace?
        testWrite("/workspace/test_write_probe_001.txt");

        // Test 3: Can we write to /tmp?
        testWrite("/tmp/test_write_probe_001.txt");

        // Test 4: Can we write to /var/tmp?
        testWrite("/var/tmp/test_write_probe_001.txt");

        // Test 5: What is the working directory?
        testWorkingDirectory();

        // Test 6: List what's in /workspace
        testList("/workspace");

        // Test 7: List what's in /tmp
        testList("/tmp");

        // Test 8: Can we read from the project directory?
        testRead("/home/engine/project/AGENTS.md");

        // Test 9: Can we create a directory?
        testCreateDirectory("/workspace/test_probe_dir_001");

        // Test 10: Can we delete the created directory?
        testDeleteDirectory("/workspace/test_probe_dir_001");

        System.out.println();
        System.out.println("=== FILESYSTEM PROBE END ===");
    }

    /**
     * Tests if we can read a file.
     * Outputs: ✓ or ✗, with specific exception details on failure
     */
    static void testRead(String path) {
        try {
            String content = new String(Files.readAllBytes(Paths.get(path)));
            String trimmed = content.length() > 100 ? content.substring(0, 100) + "..." : content;
            System.out.println("✓ READ " + path);
            System.out.println("  Content: " + trimmed.trim().replace("\n", "\\n"));
        } catch (IOException e) {
            System.out.println("✗ READ " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Tests if we can write to a file and delete it.
     * Outputs: ✓ or ✗, with specific exception details on failure
     */
    static void testWrite(String path) {
        try {
            String testData = "test_data_" + System.currentTimeMillis();
            Files.write(Paths.get(path), testData.getBytes());
            System.out.println("✓ WRITE " + path);
            System.out.println("  Action: Created file and verified write access");

            // Clean up
            Files.delete(Paths.get(path));
            System.out.println("  Cleanup: Successfully deleted test file");
        } catch (IOException e) {
            System.out.println("✗ WRITE " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Tests if we can list directory contents.
     * Outputs: ✓ or ✗, with specific exception details on failure
     */
    static void testList(String path) {
        try {
            Files.list(Paths.get(path))
                .limit(10)
                .forEach(p -> System.out.println("  - " + p.getFileName()));
            System.out.println("✓ LIST " + path);
        } catch (NoSuchFileException e) {
            System.out.println("✗ LIST " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        } catch (IOException e) {
            System.out.println("✗ LIST " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Tests what the current working directory is.
     * Always succeeds (provides factual observation)
     */
    static void testWorkingDirectory() {
        String cwd = System.getProperty("user.dir");
        System.out.println("✓ WORKING_DIRECTORY");
        System.out.println("  Path: " + cwd);
    }

    /**
     * Tests if we can create a directory.
     * Outputs: ✓ or ✗, with specific exception details on failure
     */
    static void testCreateDirectory(String path) {
        try {
            Files.createDirectory(Paths.get(path));
            System.out.println("✓ CREATE_DIRECTORY " + path);
            System.out.println("  Action: Created directory");
        } catch (IOException e) {
            System.out.println("✗ CREATE_DIRECTORY " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Tests if we can delete a directory.
     * Outputs: ✓ or ✗, with specific exception details on failure
     */
    static void testDeleteDirectory(String path) {
        try {
            Files.delete(Paths.get(path));
            System.out.println("✓ DELETE_DIRECTORY " + path);
            System.out.println("  Action: Deleted directory");
        } catch (IOException e) {
            System.out.println("✗ DELETE_DIRECTORY " + path);
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }
}

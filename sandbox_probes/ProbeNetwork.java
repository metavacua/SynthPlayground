import java.net.*;
import java.io.*;
import java.util.*;

/**
 * Network Probe - Phase 2
 *
 * Goal: Determine network capabilities and constraints through concrete testing.
 *
 * Tests three categories of network connectivity:
 * 1. DNS resolution - Can we resolve hostnames to IPs?
 * 2. TCP connectivity - Can we connect to specific ports?
 * 3. HTTP requests - Can we make HTTP GET requests?
 *
 * Design Philosophy:
 * - Each test returns specific diagnostic information (exception type + message)
 * - Output is structured for both human reading and machine parsing
 * - Tests are designed to prove/refute specific capabilities
 */
public class ProbeNetwork {
    static class NetworkTest {
        String name;
        String target;
        int port;
        String operation; // "dns", "tcp_connect", "http_get"

        NetworkTest(String name, String target, int port, String op) {
            this.name = name;
            this.target = target;
            this.port = port;
            this.operation = op;
        }
    }

    public static void main(String[] args) throws Exception {
        System.out.println("=== NETWORK PROBE START ===");
        System.out.println("Timestamp: " + java.time.Instant.now().toString());
        System.out.println();

        List<NetworkTest> tests = new ArrayList<>();

        // DNS Resolution Tests
        tests.add(new NetworkTest("dns_google", "google.com", 0, "dns"));
        tests.add(new NetworkTest("dns_openai", "api.openai.com", 0, "dns"));
        tests.add(new NetworkTest("dns_invalid", "nonexistent.invalid.domain.12345", 0, "dns"));

        // TCP Connection Tests
        tests.add(new NetworkTest("tcp_github_api", "api.github.com", 443, "tcp_connect"));
        tests.add(new NetworkTest("tcp_google_80", "google.com", 80, "tcp_connect"));
        tests.add(new NetworkTest("tcp_google_443", "google.com", 443, "tcp_connect"));
        tests.add(new NetworkTest("tcp_localhost_postgres", "localhost", 5432, "tcp_connect"));
        tests.add(new NetworkTest("tcp_localhost_mysql", "localhost", 3306, "tcp_connect"));

        // HTTP GET Tests
        tests.add(new NetworkTest("http_github_api", "http://api.github.com", 80, "http_get"));
        tests.add(new NetworkTest("http_google", "http://www.google.com", 80, "http_get"));
        tests.add(new NetworkTest("http_openai", "https://api.openai.com", 443, "http_get"));

        // Execute all tests
        for (NetworkTest test : tests) {
            runTest(test);
        }

        System.out.println();
        System.out.println("=== NETWORK PROBE END ===");
    }

    static void runTest(NetworkTest test) {
        System.out.println("TEST: " + test.name);
        System.out.println("  Target: " + test.target + (test.port > 0 ? ":" + test.port : ""));

        switch (test.operation) {
            case "dns":
                System.out.println("  Operation: DNS Resolution");
                testDns(test.target);
                break;
            case "tcp_connect":
                System.out.println("  Operation: TCP Connect");
                testTcpConnect(test.target, test.port);
                break;
            case "http_get":
                System.out.println("  Operation: HTTP GET");
                testHttpGet(test.target);
                break;
            default:
                System.out.println("  ✗ Unknown operation: " + test.operation);
        }
        System.out.println();
    }

    /**
     * Test DNS resolution.
     * Outputs: ✓ or ✗, with resolved IP address or specific error
     */
    static void testDns(String hostname) {
        try {
            InetAddress addr = InetAddress.getByName(hostname);
            System.out.println("  ✓ DNS resolved: " + hostname + " → " + addr.getHostAddress());
            System.out.println("  Observation: " + hostname + " resolved to " + addr.getHostAddress());
        } catch (UnknownHostException e) {
            System.out.println("  ✗ DNS failed: " + e.getMessage());
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - Hostname not found or DNS unavailable");
        } catch (Exception e) {
            System.out.println("  ✗ DNS error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Test TCP connection.
     * Outputs: ✓ or ✗, with connection status or specific error
     */
    static void testTcpConnect(String host, int port) {
        try {
            Socket socket = new Socket();
            socket.connect(new InetSocketAddress(host, port), 2000); // 2 second timeout
            socket.close();
            System.out.println("  ✓ TCP connection succeeded: " + host + ":" + port);
            System.out.println("  Observation: Service is listening and reachable");
        } catch (ConnectException e) {
            System.out.println("  ✗ TCP connection refused: " + e.getMessage());
            System.out.println("  Error: Service is not listening on this port");
        } catch (SocketTimeoutException e) {
            System.out.println("  ✗ TCP connection timeout");
            System.out.println("  Error: Host is not reachable within 2 seconds");
        } catch (UnknownHostException e) {
            System.out.println("  ✗ DNS resolution failed");
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        } catch (IOException e) {
            System.out.println("  ✗ TCP error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }

    /**
     * Test HTTP GET request.
     * Outputs: ✓ or ✗, with HTTP status code or specific error
     */
    static void testHttpGet(String url) {
        try {
            URL urlObj = new URL(url);
            HttpURLConnection conn = (HttpURLConnection) urlObj.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(2000); // 2 second connection timeout
            conn.setReadTimeout(2000);    // 2 second read timeout
            conn.setInstanceFollowRedirects(true);

            int code = conn.getResponseCode();
            String message = conn.getResponseMessage();

            System.out.println("  ✓ HTTP GET succeeded");
            System.out.println("  Status: " + code + " " + message);
            System.out.println("  Observation: HTTP request completed successfully");

            conn.disconnect();
        } catch (java.net.UnknownHostException e) {
            System.out.println("  ✗ HTTP error: DNS resolution failed");
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        } catch (java.net.ConnectException e) {
            System.out.println("  ✗ HTTP error: Connection refused");
            System.out.println("  Error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        } catch (java.net.SocketTimeoutException e) {
            System.out.println("  ✗ HTTP error: Request timeout");
            System.out.println("  Error: Connection or read timed out after 2 seconds");
        } catch (IOException e) {
            System.out.println("  ✗ HTTP error: " + e.getClass().getSimpleName() + " - " + e.getMessage());
        }
    }
}

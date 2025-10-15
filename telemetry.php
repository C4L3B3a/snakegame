<?php
// telemetry.php — handles telemetry logging, update checks, and admin panel

// -----------------------------
// CONFIG / FILES
// -----------------------------
$users_file = "users.json";      // JSON file storing admin username/password pairs
$telemetry_log = "telemetry.log"; // Plain-text log file storing crash reports

// -----------------------------
// HELPER FUNCTION: append telemetry
// -----------------------------
function append_telemetry($telemetry_id, $time_iso, $os, $version, $extra = '') {
    global $telemetry_log;

    // Format each entry as:
    // [telemetry_id | time_iso | OS | version | extra info]
    $entry = "[" . str_replace(["\r","\n"], '', $telemetry_id) .
             " | " . str_replace(["\r","\n"], '', $time_iso) .
             " | " . str_replace(["\r","\n"], '', $os) .
             " | " . str_replace(["\r","\n"], '', $version) .
             " | " . str_replace(["\r","\n"], ' ', $extra) . "]\n";

    // Append the entry to the telemetry log with file locking
    file_put_contents($telemetry_log, $entry, FILE_APPEND | LOCK_EX);
}

// -----------------------------
// 1 - TELEMETRY SUBMISSION
// -----------------------------
// Handles POST requests with telemetry data from client apps
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['telemetry_id'])) {
    append_telemetry(
        $_POST['telemetry_id'] ?? '',
        $_POST['time'] ?? gmdate('c'), // Use current GMT time if not provided
        $_POST['os'] ?? '',
        $_POST['version'] ?? '',
        // Include optional 'extra' info and game name
        ($_POST['extra'] ?? '') . (!empty($_POST['game']) ? " | game=".$_POST['game'] : '')
    );

    // Respond with plain text confirmation
    header('Content-Type: text/plain');
    echo "OK";
    exit;
}

// -----------------------------
// 2 - UPDATE CHECK
// -----------------------------
// Handles GET requests to check if an update is available for a specific OS
if (isset($_GET['check_update']) && isset($_GET['os'])) {
    $os = $_GET['os'];
    $version_file = 'version.json'; // JSON file storing latest versions

    if (file_exists($version_file)) {
        $versions = json_decode(file_get_contents($version_file), true);
        if (isset($versions[$os])) {
            // Respond with the latest version info and download URL
            echo json_encode([
                "update_available" => true,
                "version" => $versions[$os]["version"],
                "url" => $versions[$os]["url"]
            ]);
            exit;
        }
    }

    // Default: no update available
    echo json_encode(["update_available" => false]);
    exit;
}

// -----------------------------
// 3 - ADMIN PANEL
// -----------------------------

// Load admin users from JSON
$users = file_exists($users_file) ? json_decode(file_get_contents($users_file), true) : [];
$message = ""; // Used to display feedback (errors or success) in the panel

// -----------------------------
// UPLOAD NEW UPDATE
// -----------------------------
// Admin can upload a new version ZIP for Windows or Linux
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'upload_update') {
    $os = $_POST['os'];
    $version = $_POST['version'];
    $file = $_FILES['update_file'];

    if ($file['error'] === 0) {
        $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));

        if ($ext !== 'zip') {
            $message = "<p style='color:red;'>Only ZIP files are allowed.</p>";
        } else {
            // Ensure updates folder exists
            $target_dir = "updates/";
            if (!is_dir($target_dir)) mkdir($target_dir, 0755, true);

            // Move uploaded file to updates folder
            $filename = basename($file['name']);
            move_uploaded_file($file['tmp_name'], $target_dir . $filename);

            // Update version.json with new version info
            $version_data = file_exists('version.json') ? json_decode(file_get_contents('version.json'), true) : [];
            $version_data[$os] = [
                "version" => $version,
                "url" => "http://yourserver.com/updates/$filename" // Change to your server URL
            ];
            file_put_contents('version.json', json_encode($version_data, JSON_PRETTY_PRINT));

            $message = "<p style='color:green;'>Update uploaded successfully!</p>";
        }
    } else {
        $message = "<p style='color:red;'>Upload failed.</p>";
    }
}

// -----------------------------
// HANDLE ADMIN LOGIN
// -----------------------------
$authenticated = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['user']) && isset($_POST['pass'])) {
    $user = $_POST['user'];
    $pass = $_POST['pass'];

    if (isset($users[$user]) && $users[$user] === $pass) {
        $authenticated = true;
    } else {
        $message = "<p style='color:red;'>Invalid credentials</p>";
    }
}

// -----------------------------
// SHOW ADMIN PANEL
// -----------------------------
if ($authenticated) {
    echo "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Admin Panel</title>
          <script>
              // Toggle visibility of stack traces in telemetry
              function toggleStack(id) {
                  const el = document.getElementById('stack-' + id);
                  const btn = document.getElementById('btn-' + id);
                  if (!el) return;
                  if (el.style.display === 'none') { 
                      el.style.display='block'; 
                      btn.textContent='Hide stack'; 
                  } else { 
                      el.style.display='none'; 
                      btn.textContent='Show stack'; 
                  }
              }
          </script>
          </head><body>
          <h2>Telemetry Viewer</h2>";

    if (!empty($message)) echo $message;

    // Display telemetry logs
    if (file_exists($telemetry_log)) {
        $lines = file($telemetry_log, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        foreach ($lines as $i => $line) {
            $display = htmlspecialchars($line);
            $stack = '';
            $clean = $display;

            // Extract stack trace if present
            if (strpos($display, 'stack=') !== false) {
                [$before, $after] = explode('stack=', $display, 2);
                $clean = trim($before);
                $stack = trim($after);
            }

            echo "<div>$clean";
            if (!empty($stack)) {
                echo "<br><button id='btn-$i' onclick=\"toggleStack('$i')\">Show stack</button>";
                echo "<pre id='stack-$i' style='display:none;'>$stack</pre>";
            }
            echo "</div><hr>";
        }
    } else {
        echo "<p>No telemetry found.</p>";
    }

    // Form to upload new update ZIP
    echo "<h3>Upload New Update</h3>
          <form action='telemetry.php' method='POST' enctype='multipart/form-data'>
            OS:
            <select name='os'>
                <option>Windows</option>
                <option>Linux</option>
            </select><br>
            Version: <input type='text' name='version' required><br>
            ZIP file: <input type='file' name='update_file' accept='.zip' required><br>
            <button type='submit' name='action' value='upload_update'>Upload</button>
          </form>
          </body></html>";
    exit;
}

// -----------------------------
// DEFAULT: SHOW LOGIN FORM
// -----------------------------
echo "<!DOCTYPE html><html><head><meta charset='utf-8'><title>Admin Panel Login</title></head><body>";
if (!empty($message)) echo $message;

echo "<h3>Viewer Login</h3>
      <form action='telemetry.php' method='POST'>
        <input type='text' name='user' placeholder='Login' required><br>
        <input type='password' name='pass' placeholder='Password' required><br>
        <button type='submit'>View Telemetry</button>
      </form>";
echo "</body></html>";

// By C4L
// Notes:
// - The name of the file is telemetry.php, because it was originally intended only for telemetry logging only. But I changed my mind, but forgot to change the name. 
// - I will update this repository later with improvements and fixes, including better security (e.g., password hashing, HTTPS enforcement), and possibly a database backend.
// - And fix the name ofc.
?>
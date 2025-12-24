```
#define _GNU_SOURCE
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

// Classification of how the program became root
enum PrivSource {
    NORMAL_USER,
    SUDO_DIRECT,
    SUDO_SU_SHELL,
    SU_ROOT,
    REAL_ROOT
};

// Read parent process name from /proc/<ppid>/comm
static void get_parent_name(char *dst, size_t size) {
    pid_t ppid = getppid();
    char path[256];
    snprintf(path, sizeof(path), "/proc/%d/comm", ppid);

    FILE *f = fopen(path, "r");
    if (!f) {
        strncpy(dst, "unknown", size - 1);
        dst[size - 1] = '\0';
        return;
    }

    fgets(dst, size, f);
    dst[strcspn(dst, "\n")] = '\0';
    fclose(f);
}

// Detect privilege source
enum PrivSource detect_privilege_source() {
    uid_t uid = getuid();
    const char *sudo_uid = getenv("SUDO_UID");

    char parent[64];
    get_parent_name(parent, sizeof(parent));

    // Case 1 — Running as normal user
    if (uid != 0)
        return NORMAL_USER;

    // Now uid == 0 → running as root

    // Case 2 — sudo was involved
    if (sudo_uid != NULL) {

        // Parent = su → sudo su → ./collector
        if (strcmp(parent, "su") == 0)
            return SUDO_SU_SHELL;

        // Parent = shell → sudo ./collector
        return SUDO_DIRECT;
    }

    // sudo NOT involved → either su or real root

    // Case 3 — direct su login
    if (strcmp(parent, "su") == 0)
        return SU_ROOT;

    // Case 4 — root started the program directly
    return REAL_ROOT;
}

// Pretty print
const char* priv_to_string(enum PrivSource src) {
    switch (src) {
        case NORMAL_USER:   return "NORMAL_USER";
        case SUDO_DIRECT:   return "SUDO_DIRECT (sudo ./collector)";
        case SUDO_SU_SHELL: return "SUDO_SU_SHELL (sudo su → ./collector)";
        case SU_ROOT:       return "SU_ROOT (su - or su)";
        case REAL_ROOT:     return "REAL_ROOT (direct root execution)";
        default:            return "UNKNOWN";
    }
}

int main() {
    enum PrivSource src = detect_privilege_source();
    printf("Privilege source: %s\n", priv_to_string(src));
    return 0;
}

```
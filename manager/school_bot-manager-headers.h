#include <stdio.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <stdlib.h>


// WORKING_DIR "school_bot"

#define SCHEDULE_FILE_PATH "schedule.csv"
#define JOINER_PATH "joiner/school_bot-joiner.py"
#define LOG_PATH "logs/manager_logs.txt"
#define LESSON_NAME_MAXCHAR 16 // including null

struct session
{
    char *lesson_name;
    PROCESS_INFORMATION session_info;
};

extern char **schedule_today[9]; //schedule used by functions
extern struct tm cur_time;
extern FILE* logfile;
//modules
void load_schedule(void);
PROCESS_INFORMATION join_session(const char* lesson);
void terminate_session(PROCESS_INFORMATION session_info);
//helpers
struct tm get_time(void);

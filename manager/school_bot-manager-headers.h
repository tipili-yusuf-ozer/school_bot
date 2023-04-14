#include <stdio.h>
#include <string.h>
#include <time.h>
#include <windows.h>
//#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
//#include <crtdbg.h>



#define SCHEDULE_FILE_PATH "schedule.csv"
#define JOINER_PATH "joiner/linux/school_bot-joiner.py"
#define WORKING_DIR "../" //relative to bin
#define LESSON_NAME_MAXCHAR 16 // including null

struct session
{
    char *lesson_name;
    PROCESS_INFORMATION session_info;
};

extern char **schedule_today[9]; //schedule used by functions
extern struct tm cur_time;
//modules
void load_schedule(void);
PROCESS_INFORMATION join_session(const char* lesson);
void terminate_session(PROCESS_INFORMATION session_info);
//helpers
struct tm get_time(void);

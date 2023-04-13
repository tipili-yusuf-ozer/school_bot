#include "school_bot-manager-headers.h"



char **schedule_today[9];
const char *day_converter[]={"Mon", "Tue", "Wed", "Thu", "Fri"};

void load_schedule(void)
{

    for (int i = 0; i < 9; i++) 
    {
        schedule_today[i] = (char **) calloc(2, sizeof(char*));
        for (int n = 0; n < 2; n++)
        {
            schedule_today[i][n] = (char*)calloc(LESSON_NAME_MAXCHAR, sizeof(char));
            *schedule_today[i][n] = '0';
        }
    }
    FILE* schedule_file_ptr;
    fopen_s(&schedule_file_ptr,SCHEDULE_FILE_PATH, "r");
    if (schedule_file_ptr == NULL)
    {
        printf("schedule.csv not found, start from manager school_bot via a shortcut.");
    }
    char *schedule_file_row=(char *) calloc(120, sizeof(char));

    while(!feof(schedule_file_ptr))
    {
        char *rest1, *rest2;
        fgets(schedule_file_row, 120, schedule_file_ptr);
        char *schedule_file_row_token1=strtok_s(schedule_file_row, ",", &rest1);
        if (strcmp(schedule_file_row_token1,day_converter[(cur_time.tm_wday)-1])==0)
        {
            schedule_file_row_token1=strtok_s(NULL, ",", &rest1);
            for (int n=0; schedule_file_row_token1!=NULL; n++)
            {
                char *schedule_file_row_token2=strtok_s(schedule_file_row_token1, "|", &rest2);
                for(int m=0; schedule_file_row_token2!=NULL; m++)
                {
                    if (schedule_file_row_token2[strlen(schedule_file_row_token2) - 1] == '\n') { schedule_file_row_token2[strlen(schedule_file_row_token2) - 1] = '\0'; }
                    strncpy_s(schedule_today[n][m], LESSON_NAME_MAXCHAR * sizeof(char), schedule_file_row_token2, LESSON_NAME_MAXCHAR);
                    schedule_file_row_token2=strtok_s(NULL, "|", &rest2);
                }
                schedule_file_row_token1=strtok_s(NULL, ",", &rest1);
            }
            break; //schedule_today and schedule_file_row points to same memory so we avoid changing the value of schedule_file_row by avoiding the next fgets.
        }
    }
    free(schedule_file_row);
    fclose(schedule_file_ptr);
    free(schedule_file_ptr);

}
PROCESS_INFORMATION join_session(const char *lesson)
{
    STARTUPINFO si;
	PROCESS_INFORMATION pi;
	ZeroMemory(&si, sizeof(si));
	ZeroMemory(&pi, sizeof(pi));
	si.cb=sizeof(si);
    LPWSTR b=(wchar_t *)calloc(64, sizeof(wchar_t));
    swprintf_s(b, 63, L"python %S %S", JOINER_PATH, lesson);
    if (!CreateProcess(
        NULL,
        b,
        NULL,
        NULL,
        FALSE,
        CREATE_NO_WINDOW,
        NULL,
        NULL,
        &si,
        &pi
    ))
    {
        fprintf_s(logfile, "failed to start session for %s", lesson);
        fflush(logfile);
        printf("failed to start session for %s", lesson);
    }
    free(b);
    return pi;
}
void terminate_session(PROCESS_INFORMATION session_info)
{
    TerminateProcess(session_info.hProcess, 0);
    CloseHandle(session_info.hProcess);
    CloseHandle(session_info.hThread);
}
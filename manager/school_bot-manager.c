
#include "school_bot-manager-headers.h"

struct tm cur_time;

int main(void)
{
    cur_time=get_time();
    load_schedule();
    if (cur_time.tm_hour<8) //wait until start of schedule if opened early
    {
    struct tm start_time;
    start_time.tm_hour=8, start_time.tm_isdst=cur_time.tm_isdst, start_time.tm_mday=cur_time.tm_mday, start_time.tm_min=0, start_time.tm_mon=cur_time.tm_mon,start_time.tm_sec=0, start_time.tm_wday=cur_time.tm_wday, start_time.tm_yday=cur_time.tm_yday, start_time.tm_year=cur_time.tm_year;
    printf("waiting for schoolday to start\n");
    Sleep((mktime(&start_time)-mktime(&cur_time))*1000);
    }
    struct session active_sessions[2];
    for (int n=0; n<2; n++)
    {
        ZeroMemory(&active_sessions[n].session_info, sizeof(PROCESS_INFORMATION));
        active_sessions[n].lesson_name=(char *) calloc(LESSON_NAME_MAXCHAR, sizeof(char));
    }
    int flag = 1;
    while ((cur_time = get_time()).tm_hour<17)
    {
        printf("quitting old, starting new sessions:\n");
        //Terminate running session if they aren't included in to-be joined sessions.

        for (int n = 0; n < 2; n++)
        {

            if (flag != 1 && *(active_sessions[n].lesson_name) != '\0' && strcmp(active_sessions[n].lesson_name ,schedule_today[cur_time.tm_hour - 8][0]) && strcmp(active_sessions[n].lesson_name, schedule_today[cur_time.tm_hour - 8][1]))
            {   
                printf("terminating %s\n", active_sessions[n].lesson_name);
                terminate_session(active_sessions[n].session_info);
                *(active_sessions[n].lesson_name) = '\0';
                ZeroMemory(&active_sessions[n].session_info, sizeof(PROCESS_INFORMATION));
            }
        }
        //join sessions and write info to array
        for (int n = 0; n < 2; n++)
        {
            if ((*(schedule_today[cur_time.tm_hour - 8][n]) != '\0' && *(schedule_today[cur_time.tm_hour-8][n])!='0') && (flag == 1 || (strcmp(schedule_today[cur_time.tm_hour - 8][n], schedule_today[cur_time.tm_hour - 9][0]) && strcmp(schedule_today[cur_time.tm_hour - 8][n], schedule_today[cur_time.tm_hour - 9][1]))))
            {
                PROCESS_INFORMATION session_info = join_session(schedule_today[cur_time.tm_hour - 8][n]);
                for (int m = 0; m < 2; m++)
                {
                    if (*(active_sessions[m].lesson_name) == '\0' )
                    {

                        active_sessions[m].session_info = session_info;
                        strncpy_s(active_sessions[m].lesson_name, LESSON_NAME_MAXCHAR * sizeof(char), schedule_today[cur_time.tm_hour - 8][n], LESSON_NAME_MAXCHAR);
                        printf("started %s with pid: %d\n", active_sessions[m].lesson_name, (int) active_sessions[m].session_info.dwProcessId);
                        break;
                    }
                }
            }
        }
        struct tm next_hour;
        next_hour.tm_hour=cur_time.tm_hour+1, next_hour.tm_isdst=cur_time.tm_isdst, next_hour.tm_mday=cur_time.tm_mday, next_hour.tm_min=0, next_hour.tm_mon=cur_time.tm_mon,next_hour.tm_sec=0, next_hour.tm_wday=cur_time.tm_wday, next_hour.tm_yday=cur_time.tm_yday, next_hour.tm_year=cur_time.tm_year;
        printf("waiting until next hour\n\n\n");
        Sleep((mktime(&next_hour)-mktime(&cur_time))*1000); //sleep until beginning of the next hour
        flag=0;
    }
    //cleanup and exit
    for (int i = 0; i < 2; i++)
    {   
        if (*(active_sessions[i].lesson_name) != '\0') 
        {
            terminate_session(active_sessions[i].session_info);
        }
        free(active_sessions[i].lesson_name);
    }
    for (int i = 0; i < 9; i++)
    {
        for (int n = 0; n < 2; n++)
        {
            free(schedule_today[i][n]);
        }
        free(schedule_today[i]);
    }
}

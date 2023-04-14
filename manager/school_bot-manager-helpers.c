#include "school_bot-manager-headers.h"

struct tm get_time(void) //returns time at the moment of call
{
    struct tm tm;
    time_t timer;
    time(&timer);
    localtime_s(&tm,&timer);
    return tm;
}
#pragma once
#include <fcntl.h> 
#include <sys/stat.h> 
#include <semaphore.h> 

// Shared memory names
const char* SHM_NAME_1 = "/shm_students1";
const char* SHM_NAME_2 = "/shm_students2";

// Semaphore names
const char* SEM_PR1_DONE = "/sem_pr1_done"; // pr1 signals pr2
const char* SEM_PR2_DONE = "/sem_pr2_done"; // pr2 signals pr3


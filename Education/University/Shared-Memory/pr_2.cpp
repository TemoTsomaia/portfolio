#include "student.h"
#include "shared.h"
#include <sys/mman.h>
#include <unistd.h>
#include <vector>
#include <algorithm> // For std::sort
#include <thread>    // For std::thread
#include <iostream>
using namespace std;

struct SharedMem1Layout {
    int count;
    Student students[1000];
};

struct SharedMem2Layout {
    int count;
    Student students[50];
};

int main() {
    cout << "Process 2 starting. Waiting for Proccess 1" << endl;

    // --- Semaphore: Wait for pr1 ---
    sem_t* sem_pr1 = sem_open(SEM_PR1_DONE, 0);
    if (sem_pr1 == SEM_FAILED) {
        perror("Proccess 2 sem_open (SEM_PR1_DONE)");
        return 1;
    }
    sem_wait(sem_pr1); 
    sem_close(sem_pr1); 
    cout << "Proccess 2 Received notification from Proccess 1" << endl;



    // --- Shared Memory 1: Read ---
    int shm_fd1 = shm_open(SHM_NAME_1, O_RDONLY, 0666);
    if (shm_fd1 == -1) {
        perror("Proccess 2 shm_open (shm1)");
        return 1;
    }
    SharedMem1Layout* shm1_ptr = (SharedMem1Layout*)mmap(0, sizeof(SharedMem1Layout), PROT_READ, MAP_SHARED, shm_fd1, 0);
    if (shm1_ptr == MAP_FAILED) {
        perror("Proccess 2 mmap (shm1)");
        close(shm_fd1);
        return 1;
    }
    close(shm_fd1);



    int num_students_shm1 = shm1_ptr->count;
    vector<Student> student_list(num_students_shm1);
    if (num_students_shm1 > 0) {
        for (int i = 0; i < num_students_shm1; ++i) {
            student_list[i] = shm1_ptr->students[i];
        }
    }
    munmap(shm1_ptr, sizeof(SharedMem1Layout)); 
    cout << "Proccess 2 read " << num_students_shm1 << " students from shm1." << endl;


    // --- Calculate GPA using threads ---
    vector<thread> gpa_threads;
    cout << "Proccess 2 calculating GPAs using threads" << endl;
    for (int i = 0; i < num_students_shm1; ++i) {
        gpa_threads.emplace_back([](Student* st) {
                st->setGPA(st->getGPA());
            }, 
            &student_list[i]);
    }
    for (thread& t : gpa_threads) {
        if (t.joinable()) {
            t.join();
        }
    }
    cout << "Proccess 2 calculate GPAs" << endl;

    // --- Sort students by GPA descending ---
    sort(student_list.begin(), student_list.end(), 
        [](Student& a, Student& b) {
            return a.getGPAval() > b.getGPAval(); 
        });
    cout << "Proccess 2 students sorted by GPA" << endl;


    // --- Shared Memory 2: Write top N ---
    int shm_fd2 = shm_open(SHM_NAME_2, O_CREAT | O_RDWR, 0666);
    if (shm_fd2 == -1) {
        perror("Proccess 2 shm_open (shm2)");
        return 1;
    }

    if (ftruncate(shm_fd2, sizeof(SharedMem2Layout)) == -1) {
        perror("Proccess 2 ftruncate (shm2)");
        close(shm_fd2);
        return 1;
    }
    SharedMem2Layout* shm2_ptr = (SharedMem2Layout*)mmap(0, sizeof(SharedMem2Layout),
        PROT_READ | PROT_WRITE, MAP_SHARED, shm_fd2, 0);
    if (shm2_ptr == MAP_FAILED) {
        perror("Proccess 2 mmap (sh_mem2)");
        close(shm_fd2);
        return 1;
    }
    close(shm_fd2);

    for (int i = 0; i < 50; ++i) {
        shm2_ptr->students[i] = student_list[i];
    }
    cout << "Proccess 2 Wrote " << shm2_ptr->count << " top students to shm2." << endl;
    munmap(shm2_ptr, sizeof(SharedMem2Layout));

    // --- Semaphore: Signal pr3 ---
    sem_t* sem_pr2_done = sem_open(SEM_PR2_DONE, 0); 
    if (sem_pr2_done == SEM_FAILED) {
        perror("Proccess 2 sem_open (SEM_PR2_DONE)");
        return 1;
    }
    sem_post(sem_pr2_done); // Signal pr3
    sem_close(sem_pr2_done);
    cout << "Proccess 2 signaled pr3 (SEM_PR2_DONE)" << endl;
    std::cout << "Proccess 2 finished" << std::endl;
    return 0;
}
#include "student.h"
#include "shared.h"
#include <sys/mman.h>
#include <unistd.h>
#include <vector>
#include <iostream>
#include <iomanip> // For std::fixed, std::setprecision

struct SharedMem2Layout {
    int count;
    Student students[50];
};

int main() {
    cout << "Proccess 3 starting. Waiting for Proccess 2..." << endl;

    // --- Semaphore: Wait for pr2 ---
    sem_t* sem_pr2_done = sem_open(SEM_PR2_DONE, 0); 
    if (sem_pr2_done == SEM_FAILED) {
        perror("Proccess sem_open (SEM_PR2_DONE)");
        return 1;
    }
    sem_wait(sem_pr2_done);
    sem_close(sem_pr2_done);
    cout << "Proccess 3 Received notification from Proccess 2" << endl;

    // --- Shared Memory 2: Read ---
    int shm_fd2 = shm_open(SHM_NAME_2, O_RDONLY, 0666);
    if (shm_fd2 == -1) {
        perror("Proccess 3 shm_open (sh_mem2)");
        sem_unlink(SEM_PR1_DONE);
        sem_unlink(SEM_PR2_DONE);
        return 1;
    }


    SharedMem2Layout* shm2_ptr = (SharedMem2Layout*)mmap(0, sizeof(SharedMem2Layout), PROT_READ, MAP_SHARED, shm_fd2, 0);
    if (shm2_ptr == MAP_FAILED) {
        perror("Proccess 3 mmap (shm2)");
        close(shm_fd2);
        // Clean up shared memory and semaphores
        shm_unlink(SHM_NAME_1); 
        shm_unlink(SHM_NAME_2);
        sem_unlink(SEM_PR1_DONE);
        sem_unlink(SEM_PR2_DONE);
        return 1;
    }
    close(shm_fd2);

    int num_students_shm2 = shm2_ptr->count;
    vector<Student> top_students(num_students_shm2);
    if (num_students_shm2 > 0) {
        for (int i = 0; i < num_students_shm2; ++i) {
            top_students[i] = shm2_ptr->students[i];
        }
    }
    munmap(shm2_ptr, sizeof(SharedMem2Layout));
    cout << "Proccess 3 read " << num_students_shm2 << " students from shm2." << endl;


    // --- Analysis ---
    int students_mostly_high_grades = 0;
    for (auto& student : top_students) {
        if (student.hasMostHigh()) {
            students_mostly_high_grades++;
        }
    }
    cout << "Number of students (from top " << num_students_shm2 << ") with grades > 90 in most subjects: " << students_mostly_high_grades << "\n\n";
    cout << "Data of the first 5 students (or fewer if less than 5 available):" << endl;
    for (int i = 0; i < 5; ++i) {
        cout << top_students[i] << endl;
    }


    // --- Cleanup Shared Resources ---
    cout << "Proccess 3 cleaning up shared resources" << endl;
    if (shm_unlink(SHM_NAME_1) == -1) {
        perror("Proccess 3 shm_unlink (SHM_NAME_1)");
    }
    if (shm_unlink(SHM_NAME_2) == -1) {
        perror("Proccess 3 shm_unlink (SHM_NAME_2)");
    }
    if (sem_unlink(SEM_PR1_DONE) == -1) {
        perror("Proccess 3 sem_unlink (SEM_PR1_DONE)");
    }
    if (sem_unlink(SEM_PR2_DONE) == -1) {
        perror("Proccess 3 sem_unlink (SEM_PR2_DONE)");
    }

    cout << "Proccess 3 finished" << endl;
    return 0;
}
#include "student.h"
#include "shared.h"
#include <sys/mman.h>
#include <unistd.h>   // For ftruncate, close
#include <vector>
#include <iostream>
#include <fstream>
using namespace std;


struct SharedMem1Layout {
    int count;
    Student students[1000];
};

int main() {
    cout << "Proccess 1 is about to start!" << std::endl;

    ifstream data_in("data.in");
    if (!data_in.is_open()) {
        cerr << "Proccess 1 could not open data.in" << endl;
        return -1;
    }

    vector<Student> students;
    Student temp;
    for (int i = 0; i < 1000; i++) {
        data_in >> temp;
        students.push_back(temp);
    }


    data_in.close();
    cout << "Proccess 1 read " << students.size() << " students from data.in" << endl;

    // --- Shared Memory 1 Setup ---
    int shm_file_directory1 = shm_open(SHM_NAME_1, O_CREAT | O_RDWR, 0666);
    if (shm_file_directory1 == -1) {
        perror("Procces 1 shm_open (shm1)");
        return 1;
    }
    if (ftruncate(shm_file_directory1, sizeof(SharedMem1Layout)) == -1) {
        perror("Proccess 1 ftruncate (shm1)");
        close(shm_file_directory1);
        shm_unlink(SHM_NAME_1);
        return 1;
    }
    SharedMem1Layout* shm1_ptr = (SharedMem1Layout*)mmap(0, sizeof(SharedMem1Layout), PROT_READ | PROT_WRITE, MAP_SHARED, shm_file_directory1, 0);
    if (shm1_ptr == MAP_FAILED) {
        perror("Proccess 1 mmap (shm1)");
        close(shm_file_directory1);
        shm_unlink(SHM_NAME_1);
        return 1;
    }
    close(shm_file_directory1); 



    // Write data to shared memory
    shm1_ptr->count = students.size();
    for (size_t i = 0; i < students.size(); ++i) {
        shm1_ptr->students[i] = students[i]; 
    }
    cout << "Proccess 1 wrote " << shm1_ptr->count << " students to shm1" << endl;



    // --- Semaphore Setup & Signal ---
    // proccess 1 creates/opens semaphores. pr3 will unlink them.
    sem_t* sem_pr1 = sem_open(SEM_PR1_DONE, O_CREAT, 0666, 0);
    if (sem_pr1 == SEM_FAILED) {
        perror("Proccess 1 sem_open (SEM_PR1_DONE)");
        munmap(shm1_ptr, sizeof(SharedMem1Layout));
        shm_unlink(SHM_NAME_1);
        return 1;
    }
    sem_t* sem_pr2 = sem_open(SEM_PR2_DONE, O_CREAT, 0666, 0);
    if (sem_pr2 == SEM_FAILED) {
        perror("Proccess 1 sem_open (SEM_PR2_DONE)");
        sem_close(sem_pr1);
        sem_unlink(SEM_PR1_DONE);
        munmap(shm1_ptr, sizeof(SharedMem1Layout));
        shm_unlink(SHM_NAME_1);
        return 1;
    }
    sem_post(sem_pr1);
    cout << "Proccess 1 notified Proccess 2 (SEM_PR1_DONE)" << endl;



    // Cleanup
    munmap(shm1_ptr, sizeof(SharedMem1Layout));

    sem_close(sem_pr1);
    sem_close(sem_pr2);

    cout << "Proccess 1 finished" << endl;
    return 0;
}
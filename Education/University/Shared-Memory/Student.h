#pragma once
#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
using namespace std;


class Student {
    string ID;
    string last_name;
    string first_name;
    int* grades;
    double gpa;

public:
    Student() {
        this->grades = new int[15];
    }

    Student(istream& in) {
        this->grades = new int[15];
        in >> ID >> last_name >> first_name;
        for (int i = 0; i < 15; i++) {
            in >> grades[i];
        }

        //this->gpa = getGPA(); this will be used in proccess 2
    }

    ~Student() {
        delete[] grades;
    }

    Student& operator=(Student& other) {
        if (this == &other) {
            return *this;
        }
        last_name = other.last_name;
        first_name = other.first_name;
        gpa = other.gpa;
        for (int i = 0; i < 15; ++i) {
            grades[i] = other.grades[i];
        }
        return *this;
    }

    double getGPA() {
        double sum = 0;
        for (int i = 0; i < 15; i++) {
            sum += grades[i];
        }

        return round((sum / 15.0) * 0.04 * 100.0) / 100.0;
    }

    void setGPA(double gpa) {
        this->gpa = gpa;
    }

    double getGPAval() {
        return this->gpa;
    }

    bool hasMostHigh() {
        int high_grade_count = 0;
        for (int i = 0; i < 15; ++i) {
            if (this->grades[i] > 90) {
                high_grade_count++;
            }
        }
        return high_grade_count > (15 / 2);
    }

    friend ostream& operator<<(ostream& o, Student& st);
    friend istream& operator>>(istream& in, Student& st);
    friend bool operator>(Student& st1, Student& st2);
    friend bool operator<(Student& st1, Student& st2);

};

ostream& operator<<(ostream& o, Student& st) {
    o << st.ID <<st.last_name << st.first_name << st.gpa;
    return o;
}

istream& operator>>(istream& in, Student& st) {
    in >> st.ID >> st.last_name >> st.first_name;
    for (int i = 0; i < 15; i++) {
        in >> st.grades[i];
    }
    //st.gpa = st.getGPA(); this will be used in proccess 2
    return in;
}

bool operator>(Student& st1, Student& st2) {
    return st1.gpa > st2.gpa;
}

bool operator<(Student& st1, Student& st2) {
    return st1.gpa < st2.gpa;
}

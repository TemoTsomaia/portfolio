#include <cstring>
#include <string>
#include <fstream>
#include <unistd.h>
#include <iostream>
#include <sys/stat.h>
#include <vector>
#include <limits>
#include <filesystem>
#include <sys/wait.h>
#include <pwd.h>
using namespace std;

namespace fs = std::filesystem;


//clear console
void Clear()
{
#if defined _WIN32
	system("cls");
#elif defined (__LINUX__) || defined(__gnu_linux__) || defined(__linux__)
	system("clear");

#elif defined (__APPLE__)
	system("clear");
#endif
}

//provided by lecturer
inline bool check_file_name(const string& fileName) {
	struct stat buff;
	return (stat(fileName.c_str(), &buff) == 0);
}

void getProperInput(int& pick, int i) {
	while (true) {
		cin >> pick;

		if (cin.fail()) {
			cin.clear(); // clear error flag
			cin.ignore(numeric_limits<streamsize>::max(), '\n'); // discard bad input
			cout << "Invalid input. Try again." << endl;
			continue;
		}

		if (pick < 1 || pick > i) {
			cout << "Invalid choice. Try again." << endl;
		}
		else {
			Clear();
			break;
		}
	}
}


int getOption(initializer_list<string> options) {
	int pick;
	int i = 0;
	for (auto item : options) {
		cout << ++i << ". " << item << endl;
	}
	cout << "Choose your pick: ";
	getProperInput(pick, i);
	return pick;
}




const int N = 100; //
class myPipe {
public:
	int rdStr, // Stream to read data from pipe channel
		wrStr; // Stream to write data to pipe channel
	int dataSize;



	myPipe() : dataSize(N) {
		int tmp[2];
		if (pipe(tmp) < 0) {
			cerr << "Can't create a pipe channel!";
			exit(1);
		}
		rdStr = tmp[0];
		wrStr = tmp[1];
	}
	~myPipe() {
		close(rdStr); // Close reading stream
		close(wrStr); // Close writing stream
	}

	void RFConsole(char* buff) {
		cout << "Enter your data(only " << dataSize << " bytes will be read):";
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		cin.getline(buff, dataSize);
	}

	void WTConsole(char* buff) {
		cout << "Output of pipe: " << buff << endl;
	}

	void RFFile(const char* filename, char* buff) {
		ifstream readFile(filename);
		if (!readFile) {
			cerr << "Failed to open file for reading" << endl;
			return;
		}

		readFile.read(buff, dataSize);
		buff[readFile.gcount()] = '\0';  // Null-terminate https://cplusplus.com/reference/istream/istream/gcount/
		readFile.close();
	}

	void WTFile(string& filename, char* buff) {
		// If file doesn't exist, create it with 0640
		if (!check_file_name(filename)) {
			ofstream createFile(filename);
			createFile.close();
			chmod(filename.c_str(), 0640);
		}

		ofstream outFile(filename);
		if (!outFile) {
			cerr << "Failed to open file for writing\n";
			return;
		}
		outFile.write(buff, strlen(buff));  //strlen calculates the number of characters in the buffer up to the null terminator
		outFile.close();

	}


	size_t rd_data(char* buff) { // Read data
		size_t bytes = read(rdStr, buff, N);
		return bytes;
	}
	size_t wr_data(char* buff) { // Write data
		size_t bytes = write(wrStr, buff, N);
		return bytes;
	}
};








class GUI {
public:
	static void startGUI() {
		int pick;
		while (true) {
			cout << "Main Menu" << endl;
			pick = getOption({ "View commands", "Create an object", "Permissions" }); //main part

			switch (pick) {
			case 1:
				pick = getOption({ "Working directory", "Contents of the working directory", "Move or rename file", "Back" });
				switch (pick) {
				case 1:
					pwd();
					sleep(3);
					break;
				case 2:
					pick = getOption({ "Only visible files", "All files", "Only visible files as a list", "All files as a file" });
					switch (pick) {
					case 1:
						listCWDfilesSimple(false);
						sleep(3);
						break;
					case 2:
						listCWDfilesSimple(true);
						sleep(3);
						break;
					case 3:
						listCWDfiles(false);
						sleep(3);
						break;
					case 4:
						listCWDfiles(true);
						sleep(3);
						break;
					}
					break;


				case 3:
					moveOrRename();
					break;
				}
				break;




			case 2:
				pick = getOption({ "Directories", "Create a file", "Back" });
				switch (pick) {
				case 1:
					pick = getOption({ "Create directory", "Create directory hierarchy" });
					switch (pick) {
					case 1:
						makeDir();
						sleep(3);
						break;
					case 2:
						makeDirP();
						sleep(3);
						break;
					}
					break;


				case 2:
					touch();
					sleep(3);
					break;
				}
				break;




			case 3:
				pick = getOption({ "Add execute permission to the file owner", "Remove editing permissions from the file owner's group", "Remove read and edit permissions from other group users", "Change owner of a file", "Back" });
				switch (pick) {
				case 1:
					addExecToOwn();
					break;
				case 2:
					removeEditFromOwnGrp();
					break;
				case 3:
					removeEditFromOthers();
					break;
				case 4:
					changeOwn();
					break;
				}
				break;
			}
		}
	}







	static void pwd() {
		char cwd[1024];
		getcwd(cwd, sizeof(cwd));
		cout << "Current directory: " << cwd << endl;
	}


	static void listCWDfilesSimple(bool showHidden = false) {
		string path = ".";

		for (const auto& entry : fs::directory_iterator(path)) {
			string name = entry.path().filename().string();
			if (!showHidden && name[0] == '.') continue;
			cout << name << "  ";
		}
		cout << "\n";
	}


	static void listCWDfiles(bool showHidden = false) {
		string path = "."; // Current directory

		for (const auto& entry : fs::directory_iterator(path)) {
			string name = entry.path().filename().string();

			if (!showHidden && name[0] == '.') //In unix based system hidden files are marked by '.' in the beginning
				continue;

			fs::perms p = entry.status().permissions();

			// Print file type and permissions
			cout << (entry.is_directory() ? "d" : "-");
			cout << ((p & fs::perms::owner_read) != fs::perms::none ? "r" : "-");
			cout << ((p & fs::perms::owner_write) != fs::perms::none ? "w" : "-");
			cout << ((p & fs::perms::owner_exec) != fs::perms::none ? "x" : "-");
			cout << ((p & fs::perms::group_read) != fs::perms::none ? "r" : "-");
			cout << ((p & fs::perms::group_write) != fs::perms::none ? "w" : "-");
			cout << ((p & fs::perms::group_exec) != fs::perms::none ? "x" : "-");
			cout << ((p & fs::perms::others_read) != fs::perms::none ? "r" : "-");
			cout << ((p & fs::perms::others_write) != fs::perms::none ? "w" : "-");
			cout << ((p & fs::perms::others_exec) != fs::perms::none ? "x" : "-");
			cout << " ";

			// Print file size or dash if not a regular file
			if (fs::is_regular_file(entry)) {
				cout << setw(8) << fs::file_size(entry) << " ";
			}
			else {
				cout << setw(8) << "-" << " ";
			}

			// Print last modified time
			auto ftime = fs::last_write_time(entry);
			auto sctp = chrono::time_point_cast<chrono::system_clock::duration>(
				ftime - fs::file_time_type::clock::now()
				+ chrono::system_clock::now());
			time_t cftime = chrono::system_clock::to_time_t(sctp);
			cout << put_time(localtime(&cftime), "%Y-%m-%d %H:%M") << " ";

			cout << name << endl;
		}
	}


	static void moveOrRename() {
		string oldpath, newpath;
		cout << "Enter dir of file you want to move: ";
		cin >> oldpath;
		cout << "Enter a new path you want it relocate to(Enter old path if you want to rename it): ";
		cin >> newpath;
		if (rename(oldpath.c_str(), newpath.c_str()) == 0) {
			cout << "successfully moved/renamed " << oldpath << " to " << newpath << endl;
		}
		else {
			cerr << "Error: " << strerror(errno) << endl;
		}
	}



	static void makeDir() {
		string name;
		cout << "Provide name for directory(no spaces): ";
		cin >> name;
		if (mkdir(name.c_str(), 0777) == -1)
			cerr << "Error :  " << strerror(errno) << endl;

		else
			cout << "Directory created" << endl;
	}

	static void makeDirP() {
		string path;
		cout << "Provide path for directories: ";
		cin >> path;
		try {
			if (fs::create_directories(path)) {
				cout << "Directories created successfully: " << path << endl;
			}
			else {
				cout << "Directories already exist or couldn't be created: " << path << endl;
			}
		}
		catch (...) {
			cerr << "Something went wrong!" << endl;
		}

	}



	static void touch() {
		string filename;
		cout << "Name file you want to touch: ";
		cin >> filename;
		ofstream o(filename, ios::app);
		if (!o) {
			cerr << "Failed to open or create file: " << filename << endl;
		}
		o.close();
		cout << "Touched file: " << filename << endl;
	}


	static void addExecToOwn() {
		string filename;
		cout << "Provide the name of a file you want to act on: ";
		cin >> filename;

		struct stat filestat; //hold metadata about file
		stat(filename.c_str(), &filestat);

		mode_t newPerms = filestat.st_mode | S_IXUSR;

		if (chmod(filename.c_str(), newPerms) == -1) {
			cerr << "chmod failed: " << strerror(errno) << endl;
		}
		else {
			cout << "Permission of execute added for the owner" << endl;
		}
	}

	static void removeEditFromOwnGrp() {
		string filename;
		cout << "Provide the name of a file you want to act on: ";
		cin >> filename;

		struct stat filestat; //hold metadata about file
		stat(filename.c_str(), &filestat);

		mode_t newMode = filestat.st_mode & ~S_IWGRP;

		if (chmod(filename.c_str(), newMode) == -1) {
			cerr << "chmod failed: " << strerror(errno) << endl;
		}
		else {
			cout << "Group write permission has been removed" << endl;
		}
	}

	static void removeEditFromOthers() {
		string filename;
		cout << "Provide the name of a file you want to act on: ";
		cin >> filename;

		struct stat filestat; //hold metadata about file
		stat(filename.c_str(), &filestat);

		mode_t newMode = filestat.st_mode & ~(S_IROTH | S_IWOTH);

		if (chmod(filename.c_str(), newMode) == -1) {
			cerr << "chmod failed: " << strerror(errno) << endl;
		}
		else {
			cout << "Group write permission has been removed" << endl;
		}
	}

	static void changeOwn() {
		string filename, newOwner;
		cout << "Provide name of file you want to change owner for: ";
		cin >> filename;
		cout << "Provide name of a person you want to upgrade to owner: ";
		cin >> newOwner;


		//get new user info
		struct passwd* pw = getpwnam(newOwner.c_str());

		if (!pw) {
			cerr << "User " << newOwner << " not found" << endl;
			return;
		}

		if (chown(filename.c_str(), pw->pw_uid, -1) == -1) {
			cerr << "chown failed" << strerror(errno) << endl;
		}
		else {
			cout << "Owner of file " << filename << " has been changed to " << newOwner << endl;
		}
	}
};










int main() {
	//GUI::startGUI();
	myPipe pipe1;
	myPipe pipe2;
	pid_t pid = fork();

	if (pid < 0) {
		perror("fork");
		return 1;
	}
	else if (pid == 0) {
		// ---- CHILD ----
		char buffer[N];
		close(pipe1.wrStr);
		close(pipe2.rdStr);
		int pick;
		int initialPick;
		while (true) {
			memset(buffer, 0, N);
			pipe1.rd_data(buffer);
			int response = atoi(buffer);
			initialPick = response;
			switch (response) {
			case 1:
				pick = getOption({ "Working directory", "Contents of the working directory", "Move or rename file" });
				switch (pick) {
				case 1:
					GUI::pwd();
					sleep(3);
					break;

				case 2:
					pick = getOption({ "Only visible files", "All files", "Only visible files as a list", "All files as a file" });
					switch (pick) {
					case 1:
						GUI::listCWDfilesSimple(false);
						sleep(3);
						break;
					case 2:
						GUI::listCWDfilesSimple(true);
						sleep(3);
						break;
					case 3:
						GUI::listCWDfiles(false);
						sleep(3);
						break;
					case 4:
						GUI::listCWDfiles(true);
						sleep(3);
						break;
					}
					break;

				case 3:
					GUI::moveOrRename();
					sleep(3);
					break;
				}
				break;


			case 2:
				pick = getOption({ "Directories", "Create a file" });
				switch (pick) {
				case 1:
					pick = getOption({ "Create directory", "Create directory hierarchy" });
					switch (pick) {
					case 1:
						GUI::makeDir();
						sleep(3);
						break;
					case 2:
						GUI::makeDirP();
						sleep(3);
						break;
					}
					break;

				case 2:
					GUI::touch();
					sleep(3);
					break;
				}
				break;


			case 3:
				pick = getOption({ "Add execute permission to the file owner", "Remove editing permissions from the file owner's group", "Remove read and edit permissions from other group users", "Change owner of a file" });
				switch (pick) {
				case 1:
					GUI::addExecToOwn();
					sleep(3);
					break;
				case 2:
					GUI::removeEditFromOwnGrp();
					sleep(3);
					break;
				case 3:
					GUI::removeEditFromOthers();
					sleep(3);
					break;
				case 4:
					GUI::changeOwn();
					sleep(3);
					break;
				}
				break;


			case 4:
				pick = getOption({ "Read from console into pipe and immediately output from pipe to console", "Create a file with certain data and immediately read this data" });
				switch (pick) {
				case 1:
					pipe1.RFConsole(buffer);
					pipe2.WTConsole(buffer);
					sleep(3);
					break;
				case 2:
					pipe1.RFConsole(buffer);
					string filename = "pipe_output.txt";
					pipe2.WTFile(filename, buffer);
					cout << "Saved to " << filename << endl;
					memset(buffer, 0, N);
					pipe1.RFFile(filename.c_str(), buffer);
					pipe2.WTConsole(buffer);
					sleep(3);
					break;
				}
				break;


			case 5:
				snprintf(buffer, N, "Exit");;
				pipe2.wr_data(buffer);
				return 0;
			}
			if (initialPick != 5) {
				snprintf(buffer, N, "Restart");
				pipe2.wr_data(buffer);
			}
		}


	}
	else {
		// ---- PARENT ----
		char buffer[N];
		close(pipe1.rdStr);
		close(pipe2.wrStr);
		while (strcmp(buffer, "Exit") != 0) {
			//char buffer[N];
			memset(buffer, 0, N);
			int pick;
			cout << "Main Menu" << endl;
			pick = getOption({ "View commands", "Create an object", "Permissions","Pipe manipulation", "Exit" });
			snprintf(buffer, N, "%d", pick);
			pipe1.wr_data(buffer);

			// Receive reply
			memset(buffer, 0, N);
			pipe2.rd_data(buffer);
			cout << "[Parent] Received: " << buffer << endl;
			sleep(3);
		}
		wait(NULL); // Wait for child
	}

	return 0;
}




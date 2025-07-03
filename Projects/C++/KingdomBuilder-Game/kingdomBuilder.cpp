#include<iostream>
#include<string>
#include<vector>
#include<algorithm>
#include<limits>
#include<chrono>  // for std::chrono::seconds
#include<thread>  // for std::this_thread::sleep_for
#include<cstdlib>
#include<ctime>
#include<cctype>
using namespace std;

string strip(string& str) {
	size_t start = str.find_first_not_of(" \t\n\r\f\v"); // this finds first non-whitespace character index
	if (start == string::npos) return "";  // return empty string if all characters are whitespaces in str

	size_t end = str.find_last_not_of(" \t\n\r\f\v");  // this finds last non-whitespace character index
	return str.substr(start, end - start + 1);	//return striped string
}

void checkInt(int& a, int b = 0, int c = 0) {
	while (true) {
		if (cin >> a) {
			cin.ignore(numeric_limits<streamsize>::max(), '\n');
			if (b != 0 && (a < c || a > b)) {    // valid integer between given upper bound and given lower bound or default lower bound 
				cout << "Please enter a valid integer between 1 and " << b << ": ";
				continue; // Skip iteration
			}
			else if (a < 0) {     //checks for positive integer
				cout << "Please enter a positive integer: ";
				continue; // Skip iteration
			}
			break;
		}
		cout << "Please enter a valid integer: ";
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		//clear buffer
	}
}

void checkName(string& a) {
	while (true) {
		getline(cin, a);
		if (strip(a) == "") {  //check if string consists only from spaces...
			cout << "Name cannot consist of only white-space characters. Please enter a valid name: ";
		}
		else {
			a = strip(a);   //if not, give a the value of stripped a, and break
			break;
		}
	}
}

void clearConsole() {
#ifdef _WIN32
	system("cls"); // Windows
#else
	system("clear"); // Linux or macOS
#endif
}
//simply uses system to clear the console

void fightAnimation() {
	string c = "Fighting";
	int count = 0;
	cout << "THE FIGHT BEGINS!!!";
	this_thread::sleep_for(chrono::milliseconds(1500));
	clearConsole();
	while (count < 3) {
		for (int i = 0; i < 4; i++) {
			cout << c << endl;
			c += '.';
			this_thread::sleep_for(chrono::milliseconds(600));
			clearConsole();
		}
		c = "Fighting";
		count++;
	}
}
//this was created for animating purposes






class Kingdom {
	static vector<string> names;   //names of existing kingdoms

	string kingdomName;
	int population;
	int resources;
	vector<string> conqueredKingdoms;
	int level;
	int armyStrength;

	void calculateLevel() {
		level = population / 500;
	}
	void addResources() {
		resources += (population/500) * 50;
	}
	void armyStrengthIncrement() {
		armyStrength = armyStrength + level * level + (population / 100);
	}
public:
	bool isConquered = false;	

	Kingdom() {
		this->kingdomName = "";
		this->population = 0;
		this->resources = 0;
		this->level = 0;
		this->armyStrength = 0;
	}

	Kingdom(string kingdomName, int population, int resources, int armyStrength = 0, int level = 0, vector<string> conqueredKingdoms = {}) {
		if (find(names.begin(), names.end(), kingdomName) != names.end()) {   //checks if kingdom with given name already exists
			cerr << endl << "Kingdom with this name already exists!" << endl;
			throw invalid_argument("Please, enter unique empire name!");
		}
		else if (population == 0 || resources == 0) {	//checks if population or resources are 0
			cerr << endl << "Cannot create kingdom without population or resources!" << endl;
			throw invalid_argument("Please, enter valid empire parameters");
		}
		this->kingdomName = kingdomName;
		names.push_back(kingdomName);
		this->population = population;
		this->resources = resources;
		calculateLevel();	
		armyStrengthIncrement();	//i used this to calculate initial army strength of the kingdom
	}

	void display(ostream& o) {
		//o << "Name of Kingdom: " << kingdomName << endl;    this is commented since i show kingdom's name in remainingKingdoms() function
		o << "Population of Kingdom: " << population << endl;
		o << "Resources of Kingdom: " << resources << endl;
		if (conqueredKingdoms.empty()) {
			o << "This Kingdom has not conquered anyone else yet." << endl;
		}
		else{
			o << "Conquered Kingdoms: ";
			for (int i = 0; i < conqueredKingdoms.size()-1; i++) {
				o << conqueredKingdoms[i] << ','<<' ';
			}o<< conqueredKingdoms[conqueredKingdoms.size() - 1]<<'.'<< endl;
		}
		o << "Level of Kingdom: " << level << endl;
		o << "Army strength of Kingdom: " << armyStrength << endl;
		//if (isConquered) {												watch documentation
			//o << "This Kingdom has been conquered!"<<endl;
		//}
		//else {
			//o << "This Kingdom has not been conquered!"<<endl;
		//}
	}

	void changeName(string newName) {
		if (this->isConquered) {	//can't change name of conquered kingdom
			clearConsole();
			cout << "Cannot change name, this Kingdom is conquered!" << endl;
			this_thread::sleep_for(chrono::milliseconds(2000));
			clearConsole();
		}
		else if (this->kingdomName == newName) {	//can't input the same name as the old one
			clearConsole();
			cout << "Next time enter a new name, not the old one!" << endl;
			this_thread::sleep_for(chrono::milliseconds(2000));
			clearConsole();
		}
		else if (find(names.begin(), names.end(), newName) != names.end()) {	//can't input not unique name
			clearConsole();
			cout << "Cannot change name, kingdom with such name already exists!" << endl;
			this_thread::sleep_for(chrono::milliseconds(2000));
			clearConsole();
		}
		else {	//erases old name from vector of names, gives kingdom it's new name and adds it to vector of names
			clearConsole();
			cout << "Name of " << this->kingdomName << " has been changed to " << newName << '!';
			names.erase(remove(names.begin(), names.end(), this->kingdomName), names.end());
			this->kingdomName = newName;
			names.push_back(newName);
			this_thread::sleep_for(chrono::milliseconds(2000));
			clearConsole();
		}
	}

	void addPopulation(const int a) {
		this->population += a;
		armyStrengthIncrement();
	}	//adds population while also adding strength!

	void fight(Kingdom& other) {
		int adjustedArmyStrength = armyStrength + level * rand() % 2;;
		int enemyAdjustedArmyStrength = other.armyStrength + other.level * rand() % 2;
		if (adjustedArmyStrength > enemyAdjustedArmyStrength) {	//if initiator kingdom wins
			this->conqueredKingdoms.push_back(other.kingdomName);
			this->calculateLevel();
			this->afterWar(other);
			this->addResources();
			other.isConquered = true;  
			other.population = 0;
			other.resources = 0;
			other.level = 0;
			other.armyStrength = 0;
			for (size_t i = 0; i < other.conqueredKingdoms.size(); /* no increment here since after erase() elements are shifted down*/) {
				this->conqueredKingdoms.push_back(other.conqueredKingdoms[i]);
				other.conqueredKingdoms.erase(other.conqueredKingdoms.begin() + i);  // Erase moves elements down
			}
			other.conqueredKingdoms.clear();
		}
		else if (adjustedArmyStrength == enemyAdjustedArmyStrength) {	//if there's a draw between kingdoms
			afterWar(other);
			other.afterWar(*this);
		}
		else {		//if initiator kingdom looses
			other.conqueredKingdoms.push_back(this->kingdomName);
			other.calculateLevel();
			other.afterWar(*this);
			other.addResources();
			this->isConquered = true;
			this->population = 0;
			this->resources = 0;
			this->level = 0;
			this->armyStrength = 0;
			for (size_t i = 0; i < this->conqueredKingdoms.size();/* no increment here since after erase() elements are shifted down*/) {
				other.conqueredKingdoms.push_back(this->conqueredKingdoms[i]);
				this->conqueredKingdoms.erase(this->conqueredKingdoms.begin() + i);   // Erase moves elements down
			}
			this->conqueredKingdoms.clear();
		}
	}

	void afterWar(Kingdom& other) {   //take some of defeated kingdoms attributes, while also increasing strength in addPopulation()
		this->addPopulation(other.population / 2);
		this->resources += other.resources / 2;
		this->armyStrength += other.armyStrength / 5;
		this->level += other.level;
	}

	const string getName() {
		return kingdomName;
	}

};
vector<string> Kingdom::names;

ostream& operator<<(ostream& o, Kingdom& k1) {
	k1.display(o);
	return o;
}

void remainingKingdoms(vector<Kingdom*>& vec) {    //this is the true display of all remaining kingdoms, also numerated!
	int number = 1;
	cout << "Available Kingdoms: "<<"\n\n";
	for (auto i : vec) {
		cout << "Kingdom " << number << ":" << endl;
		cout << "Name of Kingdom: " << i->getName() << endl;
		cout << *i << "\n\n";
		number += 1;
	}cout << endl;
}
void randomFight(vector<Kingdom*>& vec) {    //random fight between two Kingdoms
	int a = rand() % vec.size(); // Random index between 0 and (size - 1)

	// Get a different random index for `b`
	int b;
	do {
		b = rand() % vec.size();
	} while (b == a); // Ensure `b` is different from `a`

	// Proceed with the fight
	clearConsole();
	vec[a]->fight(*vec[b]);
	cout << "While you were out " << vec[a]->getName() << " and " << vec[b]->getName() << " have fought!" << endl;
	this_thread::sleep_for(chrono::milliseconds(2000));
	cout << "Outcome: ";
	this_thread::sleep_for(chrono::milliseconds(1000));
	if (vec[a]->isConquered) {	
		cout << vec[b]->getName() << " has conquered " << vec[a]->getName() << '!';
		delete vec[a];    //delete defeated kingdom
		vec.erase(vec.begin() + a);    //erase it from the list, since there will be duncpointer left
	}
	else if (vec[b]->isConquered) {
		cout << vec[a]->getName() << " has conquered " << vec[b]->getName() << '!';
		delete vec[b];    //delete defeated kingdom
		vec.erase(vec.begin() + b);		//erase it from the list, since there will be duncpointer left
	}
	this_thread::sleep_for(chrono::milliseconds(3000));
	clearConsole();
}







int main() {
	srand(static_cast<unsigned int>(time(0)));    //random seed for rand()
	vector<Kingdom*> vecOfKingdoms;	   //vec of existing kingdoms
	Kingdom* userKingdom;    //Kingdom that will later be chosen by user
	int number = 1;		//only 1 variable challenge
	cout << "Please create as many kingdoms as you want and enter 'q' if you want to finish\n\n";
	while (true) {
		try {
			string name;
			int population;
			int res;
			cout << "Please enter name of Kingdom " << number << ": ";
			checkName(name);	
			if (name == "q") {	//stop asking for more kingdoms
				break;
			}
			cout << "Please enter population of Kingdom " << number << ": ";
			checkInt(population);
			cout << "Please enter resources of Kingdom " << number << ": ";
			checkInt(res);
			Kingdom* k = new Kingdom(name, population, res);	//creating kingdom, whose all keyboard-inputed attributes passed the check
			vecOfKingdoms.push_back(k);		//pushing it into the vector
			number += 1;
			cout << endl;
		}
		catch (const invalid_argument& e) {		//handle error that will be thrown by the parameterized constructor
			cerr << e.what() << "\n\n";
		}
	}


	clearConsole();
	if (vecOfKingdoms.size() < 2) {	// this block checks if there's at least 2 Kingdoms in the game
		cout << "Cannot play the game with only one or even without kingdoms!";
		return 0;	//ends the entire programm
	}

	//prompt user to choose the kingdom he wants to play for and deleting it from vector of kingdoms
	remainingKingdoms(vecOfKingdoms);	
	cout << "Choose the number of empire you want to play for: ";
	checkInt(number, vecOfKingdoms.size(), 1);
	userKingdom = (vecOfKingdoms[number - 1]);
	clearConsole();
	vecOfKingdoms.erase(vecOfKingdoms.begin() + number - 1);



	while (true) {
		cout << "You are playing for Kingdom -> " << userKingdom->getName()<<endl;
		cout << *userKingdom << "\n\n";
		
		//choose the operationg
		remainingKingdoms(vecOfKingdoms);
		cout << "1. Change name of a Kingdom"<<endl;
		cout << "2. Try to Conquer a Kingdom" << endl;
		cout << "Choose your option: ";
		checkInt(number, 2, 1);		//here, lower boundary is 1 and upper is 2


		if (number == 1) {
			string newName;
			cout << "Choose the number of empire you want to rename or '0' if you want to rename yourself: ";
			checkInt(number, vecOfKingdoms.size());   //here, lower boundary is 0, since we want user to be able to chose himself and upper is number of remaining kingdoms
			if (number == 0) {
				cout << "\nenter new name for Your Kingdom:";
				checkName(newName);
				userKingdom->changeName(newName);
			}
			else {
			cout << "\nenter new name for " << vecOfKingdoms[number - 1]->getName()<<": ";
			checkName(newName);
			vecOfKingdoms[number - 1]->changeName(newName);
			}
		}




		else if(number == 2) {
			//prompt user to choose who to fight against
			cout << "Choose the number of empire you want to try to conquer: ";
			checkInt(number, vecOfKingdoms.size(), 1);
			userKingdom->fight(*vecOfKingdoms[number - 1]);
			fightAnimation();

			if (userKingdom->isConquered) {	//if user is defeated, the game ends
				cout << "You have lost the fight against " << vecOfKingdoms[number - 1]->getName() << '!' << endl;
				this_thread::sleep_for(chrono::milliseconds(2000));
				cout << "Your Kingdom has been conquered!" << endl;
				this_thread::sleep_for(chrono::milliseconds(2000));
				cout << "GAME ";
				this_thread::sleep_for(chrono::milliseconds(500));
				cout << "OVER!";
				break;
			}
			else {	//if user won, the game continues
				cout << "You have won the fight against " << vecOfKingdoms[number - 1]->getName() << '!' << endl;
				this_thread::sleep_for(chrono::milliseconds(2000));
				cout << vecOfKingdoms[number - 1]->getName() << " is now part of your Kingdom!" << endl;
				this_thread::sleep_for(chrono::milliseconds(2000));
				cout << "Continue Expanding your empire!";
				this_thread::sleep_for(chrono::milliseconds(2000));
				clearConsole();
				delete vecOfKingdoms[number - 1];	//deleting defeated kingdom from the list
				vecOfKingdoms.erase(vecOfKingdoms.begin() + number - 1); //erase it from the list, since there will be duncpointer left
			}

			if (vecOfKingdoms.size() == 0) {  //checks whether there's any kingdom left and if not, user has finished the game
				cout << "All empires have been conquered!!!" << endl;
				this_thread::sleep_for(chrono::milliseconds(2000));
				cout << "Congratulations! you have finished the game!";
				this_thread::sleep_for(chrono::milliseconds(2000));
				break;
			}

			if (vecOfKingdoms.size() > 1) {	//if there's 2 remaining kingdoms or more, simulate fight between them
				randomFight(vecOfKingdoms);
			}

		}		
	}




	for (auto i : vecOfKingdoms) {   //deallocate the memory
		delete i;
	}
	return 0;
}
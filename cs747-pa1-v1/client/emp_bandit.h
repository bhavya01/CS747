#include <iostream>
#include <vector>
using namespace std;

class EmpBandit{
private:
	int numArms;
	vector<double> armsMeans;
	vector<int> numPulls;
public:
	EmpBandit(const int &numArms);
	void update(const int &arm,const double &reward);
	int getMaxArm();
};	
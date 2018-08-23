#include <iostream>
#include <vector>
#include <string>
#include <cmath>

#include "gsl/gsl_rng.h"
#include "gsl/gsl_randist.h"

using namespace std;

class EmpBandit{
private:
	int numArms;
	vector<double> armsMeans;
	vector<int> numPulls;

	vector<double> armsAlpha;
	vector<double> armsBeta; //used for thompson sampling
	vector<gsl_rng*> ran;

public:
	EmpBandit(const int &numArms, const int &seed);
	void update(const int &arm,const double &reward);
	int getMaxArm(string algorithm, int pulls);
	double getExpectedReward(string algorithm, double epsilon);
	double getKLUCB(int pulls, int arm, double q);
};	
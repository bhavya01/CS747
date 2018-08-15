#include "emp_bandit.h"


EmpBandit::EmpBandit(const int &numArms){
	this->numArms = numArms;
	this->armsMeans.resize(numArms,0);
	this->numPulls.resize(numArms,0);
}

void EmpBandit::update(const int &arm, const double &reward){
	//updates the empirical mean of the arm and the number of pulls
	this->numPulls[arm] += 1;
	this->armsMeans[arm] = this->armsMeans[arm] + (1.0/this->numPulls[arm])*(reward - this->armsMeans[arm]);
	return;
}

int EmpBandit::getMaxArm(string algorithm, int pulls){
	//Selects the arm with the max empirical mean
	if(algorithm.compare("epsilon-greedy") == 0)
	{
		int maxi = 0;
		double maxr = this->armsMeans[0];
		for(int i=0;i<this->numArms;i++){
			if(this->armsMeans[i]> maxr){
				maxi = i;
				maxr = this->armsMeans[i];
			}
		}
		return maxi;
	}
	else if(algorithm.compare("UCB") == 0){
		int maxi = 0;
		double maxr = this->armsMeans[0] + sqrt(2.0*log(pulls)/this->numPulls[0]);
		for(int i=0;i<this->numArms;i++){
			double t = this->armsMeans[i] + sqrt(2.0*log(pulls)/this->numPulls[i]);
			if(t > maxr){
				maxi = i;
				maxr = t;
			}
		}
		return maxi;
	}
}
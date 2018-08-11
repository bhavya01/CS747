#include "emp_bandit.h"


EmpBandit::EmpBandit(const int &numArms){
	this->numArms = numArms;
	this->armsMeans.resize(numArms,0);
	this->numPulls.resize(numArms,0);
}

void EmpBandit::update(const int &arm, const double &reward){
	this->numPulls[arm] += 1;
	this->armsMeans[arm] = this->armsMeans[arm] + (1.0/this->numPulls[arm])*(reward - this->armsMeans[arm]);
	return;
}

int EmpBandit::getMaxArm(){
	int maxi = 0;
	int maxr = this->armsMeans[0];
	for(int i=0;i<this->numArms;i++){
		if(this->armsMeans[i]> maxr){
			maxi = i;
			maxr = this->armsMeans[i];
		}
	}
	return maxi;
}
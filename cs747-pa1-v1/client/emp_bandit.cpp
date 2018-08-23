#include "emp_bandit.h"


EmpBandit::EmpBandit(const int &numArms, const int &seed){
	this->numArms = numArms;
	this->armsMeans.resize(numArms,0);
	this->numPulls.resize(numArms,0);
	this->armsAlpha.resize(numArms,1);
	this->armsBeta.resize(numArms,1);

	gsl_rng* seedGenerator = gsl_rng_alloc(gsl_rng_mt19937);
	gsl_rng_set(seedGenerator, seed);

	this->ran.clear();
	for(int a = 0; a < numArms; a++){
		this->ran.push_back(gsl_rng_alloc(gsl_rng_mt19937));
		gsl_rng_set(this->ran[a], gsl_rng_get(seedGenerator));
	}

	gsl_rng_free(seedGenerator);
}

void EmpBandit::update(const int &arm, const double &reward){
	//updates the empirical mean of the arm and the number of pulls
	this->numPulls[arm] += 1;
	this->armsMeans[arm] = this->armsMeans[arm] + (1.0/this->numPulls[arm])*(reward - this->armsMeans[arm]);

	//Check for precision errors ***********************************************************************************************
	if(reward == 1){
		this->armsAlpha[arm] += 1;
	}
	else if(reward == 0){
		this->armsBeta[arm] += 1;
	}
	return;
}
double EmpBandit::getKLUCB(int pulls, int arm, double q){
	double t = (log(pulls) + 3.0*log(log(pulls)))/this->numPulls[arm];
	if(abs(armsMeans[arm]) > 1e-8){
		t -= this->armsMeans[arm]*log(this->armsMeans[arm]/q);
	}
	if(abs(armsMeans[arm] - 1) > 1e-8){
		t -= (1.0-this->armsMeans[arm])*log((1.0-this->armsMeans[arm])/(1-q));
	}
	// cout << "Arm: " << arm << " armsMeans: "<<armsMeans[arm] << " mid: " << q <<  " pulls: " << pulls << " " << t  << endl;
	return t;
}
int EmpBandit::getMaxArm(string algorithm, int pulls){
	//Selects the arm with the max empirical mean
	if(algorithm.compare("epsilon-greedy") == 0)
	{
		int maxi = 0;
		double maxr = this->armsMeans[0];
		for(int i=1;i<this->numArms;i++){
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
		for(int i=1;i<this->numArms;i++){
			double t = this->armsMeans[i] + sqrt(2.0*log(pulls)/this->numPulls[i]);
			if(t > maxr){
				maxi = i;
				maxr = t;
			}
		}
		return maxi;
	}
	else if (algorithm.compare("KL-UCB") == 0){
		int maxi = 0;
		double maxr = 0;
		for(int i=0;i<this->numArms;i++){
			double l = this->armsMeans[i];
			if(l >= 1.0){
				maxr = 1.0;
				maxi = i;
				continue;
			}
			double r = 1.0;
			double mid =  l + (r-l)/2.0;
			int iter = 0;
			while(iter < 50){
				// cout << "Arm: " << i << " mid: " << mid<<  " pulls: " << pulls<<" "<<this->getKLUCB(pulls,i,mid) << endl;
				if(abs(this->getKLUCB(pulls,i,mid)) < 1e-6){
					break;
				}
				if(this->getKLUCB(pulls,i,mid) > 0){
					l = mid;
				}
				else if(this->getKLUCB(pulls,i,mid) <0){
					r = mid;
				}
				mid = (l+r)/2.0;
				mid = min(mid,1-1e-8);
				iter++;
			}
			if(iter == 50){
				// cout << abs(this->getKLUCB(pulls,i,mid)) << endl;
				// cout << mid<<" "<<abs(this->getKLUCB(pulls,i,mid))<<" Bisection method did not converge"<< "\n";
			}
			if(mid > maxr){
				maxr = mid;
				maxi = i;
			}
		}
		return maxi;
	}
	else if(algorithm.compare("Thompson-Sampling") == 0){
		//For Bernoulli Distribution
		int maxi = 0;
		double maxr = gsl_ran_beta(ran[0], armsAlpha[0], armsBeta[0]);
		for(int i=1;i<this->numArms;i++){
			double t = gsl_ran_beta(ran[i], armsAlpha[i], armsBeta[i]);
			if(t > maxr){
				maxi = i;
				maxr = t;
			}
		}
		return maxi;
	}
	return -1;
}

// double EmpBandit::getExpectedReward(string algorithm, double epsilon){
// 	if(algorithm.compare("epsilon-greedy") == 0)
// 	{
// 		double meanAvg = 0.0;
// 		double meanMax = 0.0;
// 		for(int i=0;i<this->numArms;i++){
// 			meanAvg += this->armsMeans[i];
// 			meanMax = max(meanMax,this->armsMeans[i]);
// 		}
// 		meanAvg = meanAvg/this->numArms;
// 		return epsilon*meanAvg + (1-epsilon)*meanMax;
// 	}
// 	return 0.0;
// }